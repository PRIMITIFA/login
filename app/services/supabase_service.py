import os
import json
import keyring
import webbrowser
import uuid
import time
from supabase import create_client, Client
from cryptography.fernet import Fernet
from PyQt6.QtCore import QObject, pyqtSignal

import logging

logger = logging.getLogger(__name__)

class SupabaseService(QObject):
    # Signals
    auth_state_changed = pyqtSignal(dict)
    auth_error = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.supabase_url = config['supabase_url']
        self.supabase_key = config['supabase_key']
        
        # Check if we're in demo mode
        self.demo_mode = (self.supabase_url == "https://demo.supabase.co" and 
                         self.supabase_key == "demo-anon-key")
        
        if self.demo_mode:
            logger.info("Running in DEMO MODE with mock authentication")
            self.client = None  # No actual Supabase client in demo mode
        else:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Successfully connected to Supabase")
            except Exception as e:
                logger.error(f"Error connecting to Supabase: {e}")
                logger.warning("Falling back to DEMO MODE with mock authentication")
                self.demo_mode = True
                self.client = None
            
        self.current_user = None
        self.current_session = None
        self.encryption_key = self._get_or_create_encryption_key()
        
        # Demo mode users (for testing)
        self.demo_users = {
            "demo@example.com": {
                "password": "password123",
                "user_id": str(uuid.uuid4()),
                "username": "demo_user",
                "role": "FREE"
            },
            "pro@example.com": {
                "password": "password123",
                "user_id": str(uuid.uuid4()),
                "username": "pro_user",
                "role": "PRO"
            }
        }
        
        # Try to restore session
        self._restore_session()
    
    def _get_or_create_encryption_key(self):
        """
        Get or create encryption key for secure storage
        """
        key = keyring.get_password("cs2_login_app", "encryption_key")
        if not key:
            key = Fernet.generate_key().decode()
            keyring.set_password("cs2_login_app", "encryption_key", key)
            logger.info("Created and saved new encryption key.")
        return key
    
    def _get_fernet(self):
        """
        Get Fernet encryption instance
        """
        return Fernet(self.encryption_key.encode())
    
    def _save_session(self, session, remember=False):
        """
        Save session data securely
        """
        if remember:
            # Encrypt session data
            fernet = self._get_fernet()
            session_data = json.dumps(session)
            encrypted_data = fernet.encrypt(session_data.encode()).decode()
            
            # Save to keyring
            keyring.set_password("cs2_login_app", "session", encrypted_data)
            logger.info("Saved session to keyring.")
    
    def _restore_session(self):
        """
        Restore previous session if available
        """
        try:
            # Get encrypted session from keyring
            encrypted_data = keyring.get_password("cs2_login_app", "session")
            if encrypted_data:
                # Decrypt session data
                fernet = self._get_fernet()
                session_data = fernet.decrypt(encrypted_data.encode()).decode()
                session = json.loads(session_data)
                logger.info("Restored session from keyring.")
                
                if self.demo_mode:
                    # For demo mode, extract user email from session token
                    # Demo tokens are in format "demo-token-{user_id}"
                    token = session.get("access_token", "")
                    
                    # Find the user with this token
                    user_email = None
                    for email, user_data in self.demo_users.items():
                        if f"demo-token-{user_data['user_id']}" == token:
                            user_email = email
                            break
                    
                    if user_email:
                        # Get demo user data
                        user_data = self.demo_users[user_email]
                        user_id = user_data["user_id"]
                        
                        # Create mock user
                        user = {
                            "id": user_id,
                            "email": user_email,
                            "user_metadata": {"username": user_data["username"]}
                        }
                        
                        self.current_user = user
                        self.current_session = session
                        
                        # Emit auth state changed signal
                        self.auth_state_changed.emit({
                            'user': self.current_user,
                            'session': self.current_session,
                            'role': user_data["role"]
                        })
                        logger.info(f"Demo user {user_email} session restored.")
                        
                        return True
                else:
                    # Set session in client
                    self.client.auth.set_session(session)
                    self.current_session = session
                    
                    # Get user from session
                    user_response = self.client.auth.get_user()
                    self.current_user = user_response.user
                    
                    # Emit auth state changed signal
                    self.auth_state_changed.emit({
                        'user': self.current_user,
                        'session': self.current_session
                    })
                    logger.info(f"User {self.current_user.email} session restored.")
                    
                    return True
        except Exception as e:
            logger.error(f"Error restoring session: {e}")
            self.clear_session()
        
        return False
    
    def clear_session(self):
        """
        Clear saved session
        """
        try:
            keyring.delete_password("cs2_login_app", "session")
            logger.info("Cleared session from keyring.")
        except:
            pass
        
        self.current_user = None
        self.current_session = None
    
    def sign_up(self, email, password, username):
        """
        Register a new user
        """
        try:
            # Handle demo mode
            if self.demo_mode:
                # Check if email already exists
                if email in self.demo_users:
                    self.auth_error.emit("Email already registered")
                    logger.warning(f"Attempted to register existing demo email: {email}")
                    return
                
                # Create new demo user
                user_id = str(uuid.uuid4())
                self.demo_users[email] = {
                    "password": password,
                    "user_id": user_id,
                    "username": username,
                    "role": "FREE"
                }
                
                # Create mock user and session
                user = {
                    "id": user_id,
                    "email": email,
                    "user_metadata": {"username": username}
                }
                
                session = {
                    "access_token": f"demo-token-{user_id}",
                    "refresh_token": f"demo-refresh-{user_id}",
                    "expires_at": int(time.time()) + 3600
                }
                
                # Set current user and session
                self.current_user = user
                self.current_session = session
                
                # Emit auth state changed signal
                self.auth_state_changed.emit({
                    'user': self.current_user,
                    'session': self.current_session
                })
                logger.info(f"Successfully signed up demo user: {email}")
                
                return
            
            # Real Supabase implementation
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            # Get user data
            user = response.user
            session = response.session
            
            if user and user.id:
                # Create profile in profiles table
                self.client.table('profiles').insert({
                    'id': user.id,
                    'username': username,
                    'role': 'FREE',
                    'created_at': 'now()'
                }).execute()
                
                # Set current user and session
                self.current_user = user
                self.current_session = session
                
                # Emit auth state changed signal
                self.auth_state_changed.emit({
                    'user': user,
                    'session': session
                })
                logger.info(f"Successfully signed up user: {email}")
                
                return True
            
            return False
        except Exception as e:
            error_msg = str(e)
            self.auth_error.emit(error_msg)
            logger.error(f"Error during sign up for {email}: {error_msg}")
            return False
    
    def sign_in(self, email, password, remember=False):
        """
        Sign in with email and password
        """
        try:
            # Handle demo mode
            if self.demo_mode:
                # Check if email exists and password matches
                if email not in self.demo_users:
                    self.auth_error.emit("Invalid email or password")
                    logger.warning(f"Failed sign in for non-existent demo user: {email}")
                    return False
                
                if self.demo_users[email]["password"] != password:
                    self.auth_error.emit("Invalid email or password")
                    logger.warning(f"Failed sign in with wrong password for demo user: {email}")
                    return False
                
                # Get demo user data
                user_data = self.demo_users[email]
                user_id = user_data["user_id"]
                
                # Create mock user and session
                user = {
                    "id": user_id,
                    "email": email,
                    "user_metadata": {"username": user_data["username"]}
                }
                
                session = {
                    "access_token": f"demo-token-{user_id}",
                    "refresh_token": f"demo-refresh-{user_id}",
                    "expires_at": int(time.time()) + 3600
                }
                
                # Set current user and session
                self.current_user = user
                self.current_session = session
                
                # Save session if remember is checked
                if remember:
                    self._save_session(session, remember)
                
                # Emit auth state changed signal
                self.auth_state_changed.emit({
                    'user': user,
                    'session': session,
                    'role': user_data["role"]
                })
                logger.info(f"Successfully signed in demo user: {email}")
                
                return True
            
            # Real Supabase implementation
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # Get user data
            user = response.user
            session = response.session
            
            # Set current user and session
            self.current_user = user
            self.current_session = session
            
            # Save session if remember is checked
            if remember:
                self._save_session(session, remember)
            
            # Emit auth state changed signal
            self.auth_state_changed.emit({
                'user': user,
                'session': session
            })
            logger.info(f"Successfully signed in user: {email}")
            
            return True
        except Exception as e:
            error_msg = str(e)
            self.auth_error.emit(error_msg)
            logger.error(f"Error during sign in for {email}: {error_msg}")
            return False
    
    def sign_in_with_oauth(self, provider, use_browser=True):
        """
        Sign in with OAuth provider
        """
        try:
            # Handle demo mode
            if self.demo_mode:
                # In demo mode, we'll simulate OAuth by using the pro@example.com account
                email = "pro@example.com"
                
                # Get demo user data
                user_data = self.demo_users[email]
                user_id = user_data["user_id"]
                
                # Create mock user and session
                user = {
                    "id": user_id,
                    "email": email,
                    "user_metadata": {"username": user_data["username"]}
                }
                
                session = {
                    "access_token": f"demo-token-{user_id}",
                    "refresh_token": f"demo-refresh-{user_id}",
                    "expires_at": int(time.time()) + 3600
                }
                
                # Set current user and session
                self.current_user = user
                self.current_session = session
                
                # Emit auth state changed signal
                self.auth_state_changed.emit({
                    'user': user,
                    'session': session,
                    'role': user_data["role"]
                })
                logger.info(f"Successfully signed in demo user via OAuth: {email}")
                
                return True
            
            # Real Supabase implementation
            response = self.client.auth.sign_in_with_oauth({
                "provider": provider,
                "options": {
                    "redirect_to": "https://yookyhounmcwvzldlnbc.supabase.co/auth/v1/callback"
                }
            })
            auth_url = response.url
            
            if use_browser:
                # Open system browser
                webbrowser.open(auth_url)
            
            logger.info(f"Redirecting to OAuth provider: {provider}")
            return auth_url
        except Exception as e:
            error_msg = str(e)
            self.auth_error.emit(error_msg)
            logger.error(f"Error during OAuth sign in with {provider}: {error_msg}")
            return None
    
    def send_password_reset_email(self, email):
        """
        Send password reset email
        """
        try:
            # Handle demo mode
            if self.demo_mode:
                if email in self.demo_users:
                    logger.info(f"Simulating password reset for demo user: {email}")
                    return True
                else:
                    self.auth_error.emit("Email not found")
                    logger.warning(f"Password reset requested for non-existent demo user: {email}")
                    return False
            
            # Real Supabase implementation
            self.client.auth.send_password_reset_email(email)
            logger.info(f"Sent password reset email to: {email}")
            return True
        except Exception as e:
            error_msg = str(e)
            self.auth_error.emit(error_msg)
            logger.error(f"Error sending password reset email to {email}: {error_msg}")
            return False
    
    def handle_oauth_callback(self, url, remember=False):
        """
        Handle OAuth callback
        """
        try:
            # Handle demo mode
            if self.demo_mode:
                # In demo mode, we've already set up the session in sign_in_with_oauth
                logger.info("Handling OAuth callback in demo mode.")
                return True
                
            # Extract session from URL
            # This is a simplified example - in a real app, you'd need to parse the URL
            # and extract the session token properly
            
            # For demonstration purposes:
            # Assume we've extracted the session token and set it
            session = self.client.auth.get_session_from_url(url)
            
            # Get user data
            user = self.client.auth.get_user()
            
            # Set current user and session
            self.current_user = user
            self.current_session = session
            
            # Save session if remember is checked
            if remember:
                self._save_session(session, remember)
            
            # Emit auth state changed signal
            self.auth_state_changed.emit({
                'user': user,
                'session': session
            })
            logger.info(f"Successfully handled OAuth callback for user: {user.email}")
            
            return True
        except Exception as e:
            error_msg = str(e)
            self.auth_error.emit(error_msg)
            logger.error(f"Error handling OAuth callback: {error_msg}")
            return False
    
    def sign_out(self):
        """
        Sign out current user
        """
        try:
            if not self.demo_mode:
                # Sign out with Supabase Auth
                self.client.auth.sign_out()
            
            # Clear session
            self.clear_session()
            
            # Emit auth state changed signal
            self.auth_state_changed.emit({
                'user': None,
                'session': None
            })
            logger.info("User signed out.")
            
            return True
        except Exception as e:
            error_msg = str(e)
            self.auth_error.emit(error_msg)
            logger.error(f"Error during sign out: {error_msg}")
            return False
    
    def get_user_role(self):
        """
        Get current user role from profiles table
        """
        if not self.current_user:
            return None
        
        try:
            # Handle demo mode
            if self.demo_mode:
                # In demo mode, find the user in demo_users by email
                user_email = self.current_user.get("email")
                if user_email and user_email in self.demo_users:
                    role = self.demo_users[user_email]["role"]
                    logger.info(f"Retrieved role for demo user {user_email}: {role}")
                    return role
                logger.warning(f"Could not find role for demo user: {user_email}")
                return "FREE"  # Default role
            
            # Real Supabase implementation
            response = self.client.table('profiles')\
                .select('role')\
                .eq('id', self.current_user.id)\
                .execute()
            
            # Get role from response
            if response.data and len(response.data) > 0:
                role = response.data[0]['role']
                logger.info(f"Retrieved role for user {self.current_user.id}: {role}")
                return role
            
            logger.warning(f"No role found for user {self.current_user.id}")
            return None
        except Exception as e:
            logger.error(f"Error getting user role: {e}")
            return None
    
    def upgrade_to_pro(self):
        """
        Upgrade user role to PRO
        """
        if not self.current_user:
            return False
        
        try:
            # Handle demo mode
            if self.demo_mode:
                # In demo mode, update the role in demo_users
                user_email = self.current_user.get("email")
                if user_email and user_email in self.demo_users:
                    self.demo_users[user_email]["role"] = "PRO"
                    
                    # Emit auth state changed signal with updated role
                    self.auth_state_changed.emit({
                        'user': self.current_user,
                        'session': self.current_session,
                        'role': "PRO"
                    })
                    logger.info(f"Upgraded demo user {user_email} to PRO.")
                    
                    return True
                logger.warning(f"Could not upgrade non-existent demo user: {user_email}")
                return False
            
            # Real Supabase implementation
            self.client.table('profiles')\
                .update({'role': 'PRO'})\
                .eq('id', self.current_user.id)\
                .execute()
            
            logger.info(f"Upgraded user {self.current_user.id} to PRO.")
            return True
        except Exception as e:
            logger.error(f"Error upgrading to PRO: {e}")
            return False