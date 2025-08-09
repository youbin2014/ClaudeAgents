#!/usr/bin/env python3
"""
Pipeline Monitor - Real-time visualization of Claude Code pipeline execution
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class PipelineMonitor:
    """Monitor and display pipeline execution status"""
    
    STAGES = {
        "routing": {"name": "Routing", "agents": ["router"]},
        "intent": {"name": "Intent Analysis", "agents": ["intent-cc", "intent-gpt5", "intent-merge-cc"]},
        "planning": {"name": "Planning", "agents": ["plan-cc", "plan-gpt5", "plan-merge-cc"]},
        "development": {"name": "Development", "agents": ["dev-cc"]},
        "evaluation": {"name": "Evaluation", "agents": ["eval-gpt5"]},
        "rollback": {"name": "Rollback", "agents": ["rollback-cc"]}
    }
    
    def __init__(self, pipeline_dir: Path = Path("./pipeline_artifacts")):
        self.pipeline_dir = pipeline_dir
        self.current_state = {}
        self.start_time = None
        
    def display_header(self, request: str):
        """Display pipeline header"""
        print("\n" + "="*60)
        print("║  🚀 DEVELOPMENT PIPELINE MONITOR")
        print("║  Request:", request[:40] + "..." if len(request) > 40 else request)
        print("║  Started:", self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else "Not started")
        print("="*60 + "\n")
    
    def display_stage_progress(self, stage_name: str, agents: List[str], current_agent: Optional[str] = None):
        """Display progress for a specific stage"""
        stage_info = self.STAGES.get(stage_name, {})
        print(f"\n📍 Stage: {stage_info.get('name', stage_name.upper())}")
        print("─" * 50)
        
        for agent in agents:
            if agent == current_agent:
                status = "⚡ ACTIVE"
                symbol = "▶"
            elif self.is_agent_completed(agent):
                status = "✅ COMPLETED"
                symbol = "✓"
            else:
                status = "⏳ PENDING"
                symbol = "○"
            
            duration = self.get_agent_duration(agent)
            duration_str = f" ({duration})" if duration else ""
            
            print(f"  {symbol} {agent:20} {status:15} {duration_str}")
    
    def display_overall_progress(self):
        """Display overall pipeline progress"""
        total_agents = sum(len(stage["agents"]) for stage in self.STAGES.values())
        completed_agents = self.count_completed_agents()
        progress_pct = (completed_agents / total_agents * 100) if total_agents > 0 else 0
        
        print("\n" + "="*60)
        print("OVERALL PROGRESS")
        print("─" * 50)
        
        # Progress bar
        bar_length = 40
        filled_length = int(bar_length * progress_pct / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        print(f"Progress: {bar} {progress_pct:.1f}%")
        print(f"Agents Completed: {completed_agents}/{total_agents}")
        
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            print(f"Elapsed Time: {self.format_duration(elapsed.total_seconds())}")
            
            if progress_pct > 0 and progress_pct < 100:
                estimated_total = elapsed.total_seconds() / (progress_pct / 100)
                remaining = estimated_total - elapsed.total_seconds()
                print(f"Estimated Remaining: {self.format_duration(remaining)}")
    
    def display_current_activity(self):
        """Display what the current agent is doing"""
        current = self.get_current_agent()
        if current:
            print("\n" + "="*60)
            print(f"🔄 CURRENT ACTIVITY: {current['agent']}")
            print("─" * 50)
            
            if current.get('status'):
                print(f"Status: {current['status']}")
            
            if current.get('output'):
                print(f"Output: {current['output'][:100]}...")
            
            if current.get('metrics'):
                print("Metrics:")
                for key, value in current['metrics'].items():
                    print(f"  - {key}: {value}")
    
    def display_stage_summary(self):
        """Display summary of all stages"""
        print("\n" + "="*60)
        print("PIPELINE STAGES")
        print("─" * 50)
        
        for stage_id, stage_info in self.STAGES.items():
            completed = self.count_stage_completed(stage_id)
            total = len(stage_info["agents"])
            
            if completed == total:
                symbol = "✅"
            elif completed > 0:
                symbol = "🔄"
            else:
                symbol = "⏳"
            
            progress = f"{completed}/{total}"
            print(f"{symbol} {stage_info['name']:20} {progress:10}")
    
    def monitor_live(self, refresh_interval: int = 2):
        """Monitor pipeline in real-time"""
        print("\033[2J\033[H")  # Clear screen
        
        while True:
            try:
                # Update state from files
                self.update_state()
                
                # Clear screen for refresh
                print("\033[2J\033[H")
                
                # Display components
                self.display_header(self.current_state.get("request", "Unknown"))
                self.display_stage_summary()
                self.display_current_activity()
                self.display_overall_progress()
                
                # Check if pipeline is complete
                if self.is_pipeline_complete():
                    print("\n" + "="*60)
                    print("✨ PIPELINE COMPLETED SUCCESSFULLY!")
                    print("="*60)
                    break
                
                time.sleep(refresh_interval)
                
            except KeyboardInterrupt:
                print("\n\nMonitoring stopped by user.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(refresh_interval)
    
    def update_state(self):
        """Update current state from pipeline artifacts"""
        state_file = self.pipeline_dir / "pipeline_state.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                self.current_state = json.load(f)
                
            if not self.start_time and self.current_state.get("started_at"):
                self.start_time = datetime.fromisoformat(self.current_state["started_at"])
    
    def get_current_agent(self) -> Optional[Dict]:
        """Get the currently active agent"""
        return self.current_state.get("current_agent")
    
    def is_agent_completed(self, agent: str) -> bool:
        """Check if an agent has completed"""
        completed = self.current_state.get("completed_agents", [])
        return agent in completed
    
    def count_completed_agents(self) -> int:
        """Count total completed agents"""
        return len(self.current_state.get("completed_agents", []))
    
    def count_stage_completed(self, stage_id: str) -> int:
        """Count completed agents in a stage"""
        stage_agents = self.STAGES[stage_id]["agents"]
        completed = self.current_state.get("completed_agents", [])
        return sum(1 for agent in stage_agents if agent in completed)
    
    def is_pipeline_complete(self) -> bool:
        """Check if pipeline is complete"""
        return self.current_state.get("status") == "completed"
    
    def get_agent_duration(self, agent: str) -> Optional[str]:
        """Get duration for a completed agent"""
        durations = self.current_state.get("agent_durations", {})
        if agent in durations:
            return self.format_duration(durations[agent])
        return None
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds/60)}m {int(seconds%60)}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

def main():
    parser = argparse.ArgumentParser(description="Monitor Claude Code Pipeline Execution")
    parser.add_argument("--pipeline-dir", default="./pipeline_artifacts",
                       help="Directory containing pipeline artifacts")
    parser.add_argument("--refresh", type=int, default=2,
                       help="Refresh interval in seconds")
    parser.add_argument("--once", action="store_true",
                       help="Display status once and exit")
    
    args = parser.parse_args()
    
    monitor = PipelineMonitor(Path(args.pipeline_dir))
    
    if args.once:
        monitor.update_state()
        monitor.display_header(monitor.current_state.get("request", "Unknown"))
        monitor.display_stage_summary()
        monitor.display_current_activity()
        monitor.display_overall_progress()
    else:
        print("Starting pipeline monitor... (Press Ctrl+C to stop)")
        monitor.monitor_live(args.refresh)

if __name__ == "__main__":
    main()