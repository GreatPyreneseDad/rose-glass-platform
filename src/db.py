"""
Rose Glass Database - Conversation and perception logging
SQLite for now, can upgrade to Postgres later
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


DB_PATH = os.getenv("ROSE_GLASS_DB", "rose_glass.db")


class RoseGlassDB:
    """Simple SQLite database for conversation logging."""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()
    
    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """Initialize database tables."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                model TEXT,
                total_exchanges INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchanges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                assistant_message TEXT,
                perception_json TEXT,
                model TEXT,
                elapsed_seconds REAL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS perception_timeseries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                psi REAL,
                rho REAL,
                q REAL,
                q_optimized REAL,
                f REAL,
                coherence REAL,
                state TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        
        # Index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_exchanges_conversation 
            ON exchanges(conversation_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timeseries_conversation 
            ON perception_timeseries(conversation_id)
        """)
        
        conn.commit()
        conn.close()
    
    def log_exchange(
        self,
        conversation_id: str,
        user_message: str,
        assistant_message: str,
        perception: Dict[str, Any],
        model: str,
        elapsed_seconds: float
    ):
        """Log a conversation exchange with perception data."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Ensure conversation exists
        cursor.execute(
            "INSERT OR IGNORE INTO conversations (id, model) VALUES (?, ?)",
            (conversation_id, model)
        )
        
        # Update exchange count
        cursor.execute(
            "UPDATE conversations SET total_exchanges = total_exchanges + 1 WHERE id = ?",
            (conversation_id,)
        )
        
        # Insert exchange
        cursor.execute("""
            INSERT INTO exchanges 
            (conversation_id, user_message, assistant_message, perception_json, model, elapsed_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            conversation_id,
            user_message,
            assistant_message,
            json.dumps(perception),
            model,
            elapsed_seconds
        ))
        
        # Insert perception timeseries
        cursor.execute("""
            INSERT INTO perception_timeseries
            (conversation_id, psi, rho, q, q_optimized, f, coherence, state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conversation_id,
            perception.get("psi", 0),
            perception.get("rho", 0),
            perception.get("q", 0),
            perception.get("q_optimized", 0),
            perception.get("f", 0),
            perception.get("coherence", 0),
            perception.get("state", "grounded")
        ))
        
        conn.commit()
        conn.close()
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get a conversation with all exchanges."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Get conversation
        cursor.execute(
            "SELECT * FROM conversations WHERE id = ?",
            (conversation_id,)
        )
        conv_row = cursor.fetchone()
        
        if not conv_row:
            conn.close()
            return None
        
        # Get exchanges
        cursor.execute(
            "SELECT * FROM exchanges WHERE conversation_id = ? ORDER BY created_at",
            (conversation_id,)
        )
        exchange_rows = cursor.fetchall()
        
        # Get perception timeseries
        cursor.execute(
            "SELECT * FROM perception_timeseries WHERE conversation_id = ? ORDER BY timestamp",
            (conversation_id,)
        )
        ts_rows = cursor.fetchall()
        
        conn.close()
        
        return {
            "id": conv_row["id"],
            "created_at": conv_row["created_at"],
            "model": conv_row["model"],
            "total_exchanges": conv_row["total_exchanges"],
            "exchanges": [
                {
                    "created_at": row["created_at"],
                    "user_message": row["user_message"],
                    "assistant_message": row["assistant_message"],
                    "perception": json.loads(row["perception_json"]),
                    "elapsed_seconds": row["elapsed_seconds"]
                }
                for row in exchange_rows
            ],
            "perception_trajectory": [
                {
                    "timestamp": row["timestamp"],
                    "psi": row["psi"],
                    "rho": row["rho"],
                    "q": row["q"],
                    "q_optimized": row["q_optimized"],
                    "f": row["f"],
                    "coherence": row["coherence"],
                    "state": row["state"]
                }
                for row in ts_rows
            ]
        }
    
    def get_recent_conversations(self, limit: int = 50) -> List[Dict]:
        """Get recent conversations summary."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                c.id,
                c.created_at,
                c.model,
                c.total_exchanges,
                e.user_message as last_user_message,
                p.coherence as last_coherence,
                p.state as last_state
            FROM conversations c
            LEFT JOIN exchanges e ON e.conversation_id = c.id
            LEFT JOIN perception_timeseries p ON p.conversation_id = c.id
            WHERE e.id = (SELECT MAX(id) FROM exchanges WHERE conversation_id = c.id)
            AND p.id = (SELECT MAX(id) FROM perception_timeseries WHERE conversation_id = c.id)
            ORDER BY c.created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "model": row["model"],
                "total_exchanges": row["total_exchanges"],
                "last_user_message": row["last_user_message"][:100] if row["last_user_message"] else None,
                "last_coherence": row["last_coherence"],
                "last_state": row["last_state"]
            }
            for row in rows
        ]
    
    def get_perception_stats(self, hours: int = 24) -> Dict:
        """Get aggregate perception statistics."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                AVG(psi) as avg_psi,
                AVG(rho) as avg_rho,
                AVG(q) as avg_q,
                AVG(f) as avg_f,
                AVG(coherence) as avg_coherence,
                COUNT(*) as total_messages,
                SUM(CASE WHEN state = 'crisis' THEN 1 ELSE 0 END) as crisis_count,
                SUM(CASE WHEN state = 'withdrawn' THEN 1 ELSE 0 END) as withdrawn_count,
                SUM(CASE WHEN state = 'activated' THEN 1 ELSE 0 END) as activated_count
            FROM perception_timeseries
            WHERE timestamp > datetime('now', ?)
        """, (f'-{hours} hours',))
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            "period_hours": hours,
            "total_messages": row["total_messages"],
            "averages": {
                "psi": round(row["avg_psi"] or 0, 3),
                "rho": round(row["avg_rho"] or 0, 3),
                "q": round(row["avg_q"] or 0, 3),
                "f": round(row["avg_f"] or 0, 3),
                "coherence": round(row["avg_coherence"] or 0, 3)
            },
            "state_counts": {
                "crisis": row["crisis_count"],
                "withdrawn": row["withdrawn_count"],
                "activated": row["activated_count"]
            }
        }


# Singleton
_db = None

def get_db() -> RoseGlassDB:
    """Get or create the database instance."""
    global _db
    if _db is None:
        _db = RoseGlassDB()
    return _db

def init_db():
    """Initialize the database."""
    get_db()
