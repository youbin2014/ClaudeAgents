#!/usr/bin/env python3
"""
Pipeline Status Display - Real-time visualization of Claude Code pipeline execution
"""

import json
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AgentStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active" 
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"


@dataclass
class AgentInfo:
    name: str
    status: AgentStatus = AgentStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status_message: str = ""
    output_preview: str = ""
    
    @property
    def elapsed_time(self) -> Optional[float]:
        if not self.start_time:
            return None
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()


@dataclass
class PipelineStage:
    name: str
    display_name: str
    agents: List[AgentInfo] = field(default_factory=list)
    status: AgentStatus = AgentStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def progress_percentage(self) -> float:
        if not self.agents:
            return 0.0
        completed = sum(1 for agent in self.agents if agent.status == AgentStatus.COMPLETED)
        return (completed / len(self.agents)) * 100
    
    @property
    def elapsed_time(self) -> Optional[float]:
        if not self.start_time:
            return None
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()


class PipelineStatusDisplay:
    """Real-time pipeline status display manager"""
    
    STAGES_CONFIG = {
        "routing": {
            "name": "routing",
            "display_name": "ROUTING", 
            "agents": ["router"]
        },
        "intent": {
            "name": "intent",
            "display_name": "INTENT ANALYSIS",
            "agents": ["intent-cc", "intent-gpt5", "intent-merge-cc"]
        },
        "planning": {
            "name": "planning", 
            "display_name": "PLANNING",
            "agents": ["plan-cc", "plan-gpt5", "plan-merge-cc"]
        },
        "development": {
            "name": "development",
            "display_name": "DEVELOPMENT", 
            "agents": ["dev-cc"]
        },
        "evaluation": {
            "name": "evaluation",
            "display_name": "EVALUATION",
            "agents": ["eval-gpt5"]
        },
        "rollback": {
            "name": "rollback",
            "display_name": "ROLLBACK",
            "agents": ["rollback-cc"]
        }
    }
    
    STATUS_ICONS = {
        AgentStatus.PENDING: "📋",
        AgentStatus.ACTIVE: "⚡",
        AgentStatus.COMPLETED: "✅", 
        AgentStatus.FAILED: "❌",
        AgentStatus.WAITING: "⏳"
    }
    
    def __init__(self, request: str, pipeline_id: str = None):
        self.request = request
        self.pipeline_id = pipeline_id or f"pip_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = datetime.now()
        self.current_stage: Optional[str] = None
        self.stages: Dict[str, PipelineStage] = {}
        self.total_estimated_duration = timedelta(minutes=25)  # Default estimate
        self.display_lock = threading.Lock()
        
        # Initialize stages
        for stage_key, config in self.STAGES_CONFIG.items():
            stage = PipelineStage(
                name=config["name"],
                display_name=config["display_name"]
            )
            for agent_name in config["agents"]:
                stage.agents.append(AgentInfo(name=agent_name))
            self.stages[stage_key] = stage
    
    def start_pipeline(self, mode: str = "pipeline-direct"):
        """Display pipeline startup header"""
        with self.display_lock:
            self._clear_screen()
            print(self._get_header(mode))
            print(self._get_stage_overview())
            print(f"\n💬 Pipeline starting...")
    
    def update_stage(self, stage_name: str, status: AgentStatus = AgentStatus.ACTIVE):
        """Update current stage status"""
        with self.display_lock:
            if stage_name in self.stages:
                stage = self.stages[stage_name]
                stage.status = status
                if status == AgentStatus.ACTIVE and not stage.start_time:
                    stage.start_time = datetime.now()
                elif status == AgentStatus.COMPLETED and not stage.end_time:
                    stage.end_time = datetime.now()
                
                self.current_stage = stage_name
                self._refresh_display()
    
    def set_agent_status(self, agent_name: str, status: AgentStatus, 
                        status_message: str = "", output_preview: str = ""):
        """Update individual agent status"""
        with self.display_lock:
            agent = self._find_agent(agent_name)
            if agent:
                agent.status = status
                agent.status_message = status_message
                agent.output_preview = output_preview
                
                if status == AgentStatus.ACTIVE and not agent.start_time:
                    agent.start_time = datetime.now()
                elif status in [AgentStatus.COMPLETED, AgentStatus.FAILED] and not agent.end_time:
                    agent.end_time = datetime.now()
                    agent.duration = agent.elapsed_time
                
                self._refresh_display()
    
    def agent_started(self, agent_name: str, status_message: str = ""):
        """Mark agent as started/active"""
        self.set_agent_status(agent_name, AgentStatus.ACTIVE, status_message)
    
    def agent_completed(self, agent_name: str, duration: float = None, output_preview: str = ""):
        """Mark agent as completed"""
        agent = self._find_agent(agent_name)
        if agent and duration:
            agent.duration = duration
        self.set_agent_status(agent_name, AgentStatus.COMPLETED, "Completed successfully", output_preview)
    
    def agent_failed(self, agent_name: str, error_message: str):
        """Mark agent as failed"""
        self.set_agent_status(agent_name, AgentStatus.FAILED, f"Error: {error_message}")
    
    def display_user_confirmation(self, stage: str, summary: Dict[str, Any]) -> bool:
        """Display user confirmation prompt"""
        with self.display_lock:
            print(f"\n🤔 USER CONFIRMATION REQUIRED")
            print("━" * 60)
            print(f"\nStage: {stage}")
            print(f"Result: {summary.get('summary', 'Stage completed')}")
            
            if 'key_points' in summary:
                print("\nKey Points:")
                for point in summary['key_points']:
                    print(f"• {point}")
            
            print(f"\n❓ Proceed with this result? (y/n): ", end="", flush=True)
            
            # In a real implementation, this would handle user input
            # For now, we'll simulate automatic approval
            return True
    
    def pipeline_completed(self, success: bool = True, summary: Dict[str, Any] = None):
        """Display pipeline completion status"""
        with self.display_lock:
            end_time = datetime.now()
            total_duration = (end_time - self.start_time).total_seconds()
            
            print(f"\n{'🎉' if success else '❌'} PIPELINE {'COMPLETED' if success else 'FAILED'}")
            print("━" * 60)
            print(f"Total Duration: {self._format_duration(total_duration)}")
            print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if summary:
                print(f"\nSummary: {summary.get('summary', 'Pipeline execution completed')}")
            
            print("\n" + "=" * 60)
    
    def display_error(self, error: str, stage: str = None, agent: str = None):
        """Display error information"""
        with self.display_lock:
            print(f"\n❌ PIPELINE ERROR")
            print("━" * 60)
            if stage:
                print(f"Stage: {stage}")
            if agent:
                print(f"Agent: {agent}")
            print(f"Error: {error}")
            print()
    
    def _find_agent(self, agent_name: str) -> Optional[AgentInfo]:
        """Find agent by name across all stages"""
        for stage in self.stages.values():
            for agent in stage.agents:
                if agent.name == agent_name:
                    return agent
        return None
    
    def _refresh_display(self):
        """Refresh the entire display"""
        self._clear_screen()
        print(self._get_header())
        print(self._get_stage_display())
        print(self._get_progress_bar())
        print(self._get_current_activity())
    
    def _clear_screen(self):
        """Clear the terminal screen"""
        print("\033[2J\033[H", end="")
    
    def _get_header(self, mode: str = "pipeline") -> str:
        """Generate pipeline header"""
        mode_display = "PIPELINE MODE ACTIVATED" if mode == "pipeline-direct" else "DEVELOPMENT PIPELINE"
        if mode == "pipeline-direct":
            mode_display += " (/pipeline command)"
        
        header = f"🚀 {mode_display}\n"
        header += "━" * 60 + "\n"
        header += f"Request: {self.request[:50]}{'...' if len(self.request) > 50 else ''}\n"
        header += f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"Pipeline ID: {self.pipeline_id}"
        return header
    
    def _get_stage_overview(self) -> str:
        """Generate stage overview"""
        overview = "\nPIPELINE STAGES:\n"
        stage_indicators = []
        
        for stage_key, stage in self.stages.items():
            if stage_key == "rollback":  # Skip rollback in overview unless needed
                continue
                
            if stage.status == AgentStatus.COMPLETED:
                indicator = "[✅]"
            elif stage.status == AgentStatus.ACTIVE:
                indicator = "[⚡]"
            elif stage.status == AgentStatus.FAILED:
                indicator = "[❌]"  
            else:
                indicator = "[ ]"
            
            stage_indicators.append(f"{indicator} {stage.display_name}")
        
        overview += " → ".join(stage_indicators)
        return overview
    
    def _get_stage_display(self) -> str:
        """Generate current stage detailed display"""
        if not self.current_stage or self.current_stage not in self.stages:
            return ""
        
        stage = self.stages[self.current_stage]
        stage_num = list(self.stages.keys()).index(self.current_stage) + 1
        total_stages = len(self.stages) - 1  # Exclude rollback from count
        
        display = f"\n📍 Stage {stage_num}/{total_stages}: {stage.display_name}"
        if stage.elapsed_time:
            display += f" ({self._format_duration(stage.elapsed_time)})"
        display += "\n" + "─" * 60 + "\n"
        
        for agent in stage.agents:
            icon = self.STATUS_ICONS[agent.status]
            status_text = agent.status.value.upper()
            duration_text = f"({self._format_duration(agent.duration)})" if agent.duration else ""
            
            display += f"├─ [{icon}] {agent.name:15} {status_text:12} {duration_text}\n"
            
            if agent.status_message and agent.status == AgentStatus.ACTIVE:
                display += f"│   💬 {agent.status_message}\n"
        
        return display
    
    def _get_progress_bar(self) -> str:
        """Generate overall progress bar"""
        total_agents = sum(len(stage.agents) for stage in self.stages.values())
        completed_agents = sum(
            sum(1 for agent in stage.agents if agent.status == AgentStatus.COMPLETED)
            for stage in self.stages.values()
        )
        
        progress_pct = (completed_agents / total_agents * 100) if total_agents > 0 else 0
        
        # Progress bar visualization
        bar_length = 40
        filled_length = int(bar_length * progress_pct / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        elapsed_str = self._format_duration(elapsed)
        
        # Estimate remaining time
        if progress_pct > 0:
            estimated_total = elapsed / (progress_pct / 100)
            remaining = max(0, estimated_total - elapsed)
            remaining_str = self._format_duration(remaining)
        else:
            remaining_str = "Calculating..."
        
        progress = f"\nProgress: {bar} {progress_pct:.1f}%\n"
        progress += f"Elapsed: {elapsed_str} | Est. Remaining: {remaining_str}"
        
        return progress
    
    def _get_current_activity(self) -> str:
        """Generate current activity description"""
        if not self.current_stage:
            return ""
        
        stage = self.stages[self.current_stage]
        active_agent = next((agent for agent in stage.agents if agent.status == AgentStatus.ACTIVE), None)
        
        if active_agent:
            activity = f"\n💬 Current: {active_agent.name}"
            if active_agent.status_message:
                activity += f" - {active_agent.status_message}"
            return activity
        
        return ""
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"


class PipelineStatusManager:
    """Singleton manager for pipeline status display"""
    
    _instance = None
    _display: Optional[PipelineStatusDisplay] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def start_pipeline(cls, request: str, mode: str = "pipeline", pipeline_id: str = None):
        """Start a new pipeline status display"""
        instance = cls()
        instance._display = PipelineStatusDisplay(request, pipeline_id)
        instance._display.start_pipeline(mode)
        return instance._display
    
    @classmethod
    def get_display(cls) -> Optional[PipelineStatusDisplay]:
        """Get current pipeline display"""
        instance = cls()
        return instance._display
    
    @classmethod
    def clear_display(cls):
        """Clear current display"""
        instance = cls()
        instance._display = None


# Convenience functions for easy integration
def start_pipeline_display(request: str, mode: str = "pipeline") -> PipelineStatusDisplay:
    """Start pipeline status display"""
    return PipelineStatusManager.start_pipeline(request, mode)


def get_pipeline_display() -> Optional[PipelineStatusDisplay]:
    """Get current pipeline display"""
    return PipelineStatusManager.get_display()


def update_agent_status(agent_name: str, status: str, message: str = ""):
    """Update agent status (convenience function)"""
    display = get_pipeline_display()
    if display:
        agent_status = AgentStatus(status.lower())
        display.set_agent_status(agent_name, agent_status, message)


# Example usage and testing
if __name__ == "__main__":
    # Demo the status display
    display = start_pipeline_display(
        request="Convert authentication system to async with comprehensive tests",
        mode="pipeline-direct"
    )
    
    try:
        # Simulate pipeline execution
        time.sleep(1)
        
        # Stage 1: Intent Analysis
        display.update_stage("intent", AgentStatus.ACTIVE)
        display.agent_started("intent-cc", "Analyzing user request and code context...")
        time.sleep(2)
        display.agent_completed("intent-cc", 2.0, "Found 5 auth-related files")
        
        display.agent_started("intent-gpt5", "GPT-5 analyzing code touchpoints...")
        time.sleep(3)
        display.agent_completed("intent-gpt5", 3.0, "Identified 12 functions to modify")
        
        display.agent_started("intent-merge-cc", "Merging analysis results...")
        time.sleep(1)
        display.agent_completed("intent-merge-cc", 1.0, "Comprehensive intent created")
        
        # Stage 2: Planning
        display.update_stage("planning", AgentStatus.ACTIVE)
        display.agent_started("plan-cc", "Creating TDD-focused development plan...")
        time.sleep(3)
        display.agent_completed("plan-cc", 3.0, "Generated 15 test cases")
        
        print("\n⏸️  Demo completed. Press Ctrl+C to exit.")
        
        # Keep display alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        display.pipeline_completed(True, {"summary": "Demo completed successfully"})
        print("\nDemo finished.")