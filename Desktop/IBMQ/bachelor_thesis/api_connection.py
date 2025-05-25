import os
import dotenv
from pathlib import Path
from qiskit_ibm_runtime import QiskitRuntimeService
class QiskitService:
    def __init__(self, api_key_path: str):
        self.api_key_path = Path(api_key_path)
        self.service = None
        self._load_api_key()
        self._connect_service()
        self.backend = None
    
    def _load_api_key(self):
        dotenv.load_dotenv(self.api_key_path)
        self.api_key = os.getenv("IBM_Q_API_KEY")
        if not self.api_key:
            raise ValueError("IBM_Q_API_KEY not found in environment variables")
    
    def _connect_service(self):
        self.service = QiskitRuntimeService(channel="ibm_quantum", token=self.api_key)
        print("Connected to IBM Quantum.")
    
    def get_active_account(self):
        return self.service.active_account()
    
    def get_backends(self, min_qubits=13):
        return self.service.backends(min_num_qubits=min_qubits)
    
    def get_least_busy_backend(self):
        return self.service.least_busy()
    
    def check_pending_jobs(self):
        return self.service.check_pending_jobs()
    
    def get_saved_accounts(self):
        return self.service.saved_accounts()
    
    def get_usage(self):
        return self.service.usage()
    
    def connect_to_backend(self, backend_name = None):
        if backend_name is None:
            self.backend = self.service.least_busy()
            print(f"Connected to least busy backend: {self.backend.name}")
            return self.backend
        else:
            try:
                # Change backends() to backend() to get a single backend object, not a list
                self.backend = self.service.backend(name=backend_name)
                print(f"Connected to backend: {backend_name}")
                return self.backend 
            except Exception as e:
                print(f"Error connecting to backend {backend_name}: {e}")
                return None