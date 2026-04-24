"""
Role-Based Access Control (RBAC) System
Manages user roles and permissions for the banking model validation system
"""

from enum import Enum
from typing import List, Dict, Set, Optional
from datetime import datetime
from loguru import logger


class Role(str, Enum):
    """User roles in the system"""
    ADMIN = "admin"
    MODEL_MANAGER = "model_manager"
    MODEL_VALIDATOR = "model_validator"
    MODEL_DEVELOPER = "model_developer"
    COMPLIANCE_OFFICER = "compliance_officer"
    AUDITOR = "auditor"
    VIEWER = "viewer"


class Permission(str, Enum):
    """System permissions"""
    # Model Management
    CREATE_MODEL = "create_model"
    VIEW_MODEL = "view_model"
    EDIT_MODEL = "edit_model"
    DELETE_MODEL = "delete_model"
    DEPLOY_MODEL = "deploy_model"
    
    # Validation
    CREATE_VALIDATION = "create_validation"
    VIEW_VALIDATION = "view_validation"
    EDIT_VALIDATION = "edit_validation"
    APPROVE_VALIDATION = "approve_validation"
    REJECT_VALIDATION = "reject_validation"
    
    # Monitoring
    VIEW_MONITORING = "view_monitoring"
    CONFIGURE_MONITORING = "configure_monitoring"
    MANAGE_ALERTS = "manage_alerts"
    
    # Governance
    VIEW_GOVERNANCE = "view_governance"
    EDIT_GOVERNANCE = "edit_governance"
    VIEW_COMPLIANCE = "view_compliance"
    GENERATE_REPORTS = "generate_reports"
    
    # Workflows
    CREATE_WORKFLOW = "create_workflow"
    VIEW_WORKFLOW = "view_workflow"
    APPROVE_TASK = "approve_task"
    REJECT_TASK = "reject_task"
    
    # Documentation
    VIEW_DOCUMENTATION = "view_documentation"
    EDIT_DOCUMENTATION = "edit_documentation"
    SIGN_DOCUMENTATION = "sign_documentation"
    
    # Administration
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    VIEW_AUDIT_LOG = "view_audit_log"
    SYSTEM_SETTINGS = "system_settings"


# Role-Permission Mapping
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        # Full access to everything
        Permission.CREATE_MODEL,
        Permission.VIEW_MODEL,
        Permission.EDIT_MODEL,
        Permission.DELETE_MODEL,
        Permission.DEPLOY_MODEL,
        Permission.CREATE_VALIDATION,
        Permission.VIEW_VALIDATION,
        Permission.EDIT_VALIDATION,
        Permission.APPROVE_VALIDATION,
        Permission.REJECT_VALIDATION,
        Permission.VIEW_MONITORING,
        Permission.CONFIGURE_MONITORING,
        Permission.MANAGE_ALERTS,
        Permission.VIEW_GOVERNANCE,
        Permission.EDIT_GOVERNANCE,
        Permission.VIEW_COMPLIANCE,
        Permission.GENERATE_REPORTS,
        Permission.CREATE_WORKFLOW,
        Permission.VIEW_WORKFLOW,
        Permission.APPROVE_TASK,
        Permission.REJECT_TASK,
        Permission.VIEW_DOCUMENTATION,
        Permission.EDIT_DOCUMENTATION,
        Permission.SIGN_DOCUMENTATION,
        Permission.MANAGE_USERS,
        Permission.MANAGE_ROLES,
        Permission.VIEW_AUDIT_LOG,
        Permission.SYSTEM_SETTINGS,
    },
    
    Role.MODEL_MANAGER: {
        # Can manage models, approve validations, view all data
        Permission.CREATE_MODEL,
        Permission.VIEW_MODEL,
        Permission.EDIT_MODEL,
        Permission.DEPLOY_MODEL,
        Permission.VIEW_VALIDATION,
        Permission.APPROVE_VALIDATION,
        Permission.REJECT_VALIDATION,
        Permission.VIEW_MONITORING,
        Permission.CONFIGURE_MONITORING,
        Permission.MANAGE_ALERTS,
        Permission.VIEW_GOVERNANCE,
        Permission.EDIT_GOVERNANCE,
        Permission.VIEW_COMPLIANCE,
        Permission.GENERATE_REPORTS,
        Permission.VIEW_WORKFLOW,
        Permission.APPROVE_TASK,
        Permission.REJECT_TASK,
        Permission.VIEW_DOCUMENTATION,
        Permission.SIGN_DOCUMENTATION,
        Permission.VIEW_AUDIT_LOG,
    },
    
    Role.MODEL_VALIDATOR: {
        # Can create and edit validations, view models, use governance features
        Permission.VIEW_MODEL,
        Permission.CREATE_VALIDATION,
        Permission.VIEW_VALIDATION,
        Permission.EDIT_VALIDATION,
        Permission.VIEW_MONITORING,
        Permission.VIEW_GOVERNANCE,
        Permission.VIEW_COMPLIANCE,
        Permission.GENERATE_REPORTS,
        Permission.VIEW_WORKFLOW,
        Permission.VIEW_DOCUMENTATION,
        Permission.EDIT_DOCUMENTATION,
    },
    
    Role.MODEL_DEVELOPER: {
        # Can create models, view validations
        Permission.CREATE_MODEL,
        Permission.VIEW_MODEL,
        Permission.EDIT_MODEL,
        Permission.VIEW_VALIDATION,
        Permission.VIEW_MONITORING,
        Permission.VIEW_GOVERNANCE,
        Permission.VIEW_DOCUMENTATION,
    },
    
    Role.COMPLIANCE_OFFICER: {
        # Can view everything, generate reports, manage compliance
        Permission.VIEW_MODEL,
        Permission.VIEW_VALIDATION,
        Permission.VIEW_MONITORING,
        Permission.VIEW_GOVERNANCE,
        Permission.EDIT_GOVERNANCE,
        Permission.VIEW_COMPLIANCE,
        Permission.GENERATE_REPORTS,
        Permission.VIEW_WORKFLOW,
        Permission.VIEW_DOCUMENTATION,
        Permission.VIEW_AUDIT_LOG,
    },
    
    Role.AUDITOR: {
        # Read-only access to everything
        Permission.VIEW_MODEL,
        Permission.VIEW_VALIDATION,
        Permission.VIEW_MONITORING,
        Permission.VIEW_GOVERNANCE,
        Permission.VIEW_COMPLIANCE,
        Permission.VIEW_WORKFLOW,
        Permission.VIEW_DOCUMENTATION,
        Permission.VIEW_AUDIT_LOG,
    },
    
    Role.VIEWER: {
        # Basic read-only access
        Permission.VIEW_MODEL,
        Permission.VIEW_VALIDATION,
        Permission.VIEW_DOCUMENTATION,
    },
}


class User:
    """User model with role and permissions"""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str,
        role: Role,
        full_name: Optional[str] = None,
        department: Optional[str] = None
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.role = role
        self.full_name = full_name or username
        self.department = department
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.is_active = True
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        return permission in ROLE_PERMISSIONS.get(self.role, set())
    
    def has_any_permission(self, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions"""
        return any(self.has_permission(p) for p in permissions)
    
    def has_all_permissions(self, permissions: List[Permission]) -> bool:
        """Check if user has all of the specified permissions"""
        return all(self.has_permission(p) for p in permissions)
    
    def get_permissions(self) -> Set[Permission]:
        """Get all permissions for the user's role"""
        return ROLE_PERMISSIONS.get(self.role, set())
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "full_name": self.full_name,
            "department": self.department,
            "permissions": [p.value for p in self.get_permissions()],
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
        }


class RBACManager:
    """Manages role-based access control"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        logger.info("RBAC Manager initialized")
    
    def create_user(
        self,
        username: str,
        email: str,
        role: Role,
        full_name: Optional[str] = None,
        department: Optional[str] = None
    ) -> User:
        """Create a new user"""
        user_id = f"USER_{datetime.utcnow().timestamp()}"
        user = User(user_id, username, email, role, full_name, department)
        self.users[user_id] = user
        logger.info(f"Created user: {username} with role: {role.value}")
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def update_user_role(self, user_id: str, new_role: Role) -> bool:
        """Update user's role"""
        user = self.get_user(user_id)
        if user:
            old_role = user.role
            user.role = new_role
            logger.info(f"Updated user {user.username} role from {old_role.value} to {new_role.value}")
            return True
        return False
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user"""
        user = self.get_user(user_id)
        if user:
            user.is_active = False
            logger.info(f"Deactivated user: {user.username}")
            return True
        return False
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has permission"""
        user = self.get_user(user_id)
        if not user or not user.is_active:
            return False
        return user.has_permission(permission)
    
    def get_role_permissions(self, role: Role) -> Set[Permission]:
        """Get all permissions for a role"""
        return ROLE_PERMISSIONS.get(role, set())
    
    def list_users(self, role: Optional[Role] = None) -> List[User]:
        """List all users, optionally filtered by role"""
        users = list(self.users.values())
        if role:
            users = [u for u in users if u.role == role]
        return users
    
    def get_user_dashboard_config(self, user_id: str) -> Dict:
        """Get dashboard configuration based on user role"""
        user = self.get_user(user_id)
        if not user:
            return {}
        
        # Role-specific dashboard configurations
        configs = {
            Role.ADMIN: {
                "widgets": ["system_health", "user_activity", "model_inventory", "alerts", "compliance"],
                "default_view": "overview",
                "can_customize": True,
            },
            Role.MODEL_MANAGER: {
                "widgets": ["model_inventory", "validation_queue", "deployment_status", "alerts", "bottlenecks"],
                "default_view": "management",
                "can_customize": True,
            },
            Role.MODEL_VALIDATOR: {
                "widgets": ["validation_queue", "model_stages", "governance_status", "my_tasks", "documentation"],
                "default_view": "validation",
                "can_customize": True,
            },
            Role.MODEL_DEVELOPER: {
                "widgets": ["my_models", "validation_status", "performance_metrics", "documentation"],
                "default_view": "development",
                "can_customize": False,
            },
            Role.COMPLIANCE_OFFICER: {
                "widgets": ["compliance_status", "audit_trail", "reports", "upcoming_reviews"],
                "default_view": "compliance",
                "can_customize": True,
            },
            Role.AUDITOR: {
                "widgets": ["audit_trail", "compliance_reports", "model_inventory", "documentation"],
                "default_view": "audit",
                "can_customize": False,
            },
            Role.VIEWER: {
                "widgets": ["model_inventory", "documentation"],
                "default_view": "view",
                "can_customize": False,
            },
        }
        
        return configs.get(user.role, {})


# Global RBAC manager instance
rbac_manager = RBACManager()


# Helper functions for permission checking
def require_permission(permission: Permission):
    """Decorator to require specific permission"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would integrate with FastAPI's dependency injection
            # For now, it's a placeholder
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permissions: List[Permission]):
    """Decorator to require any of the specified permissions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role: Role):
    """Decorator to require specific role"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Made with ❤️ by Bob

# Made with Bob
