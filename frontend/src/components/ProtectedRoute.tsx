import { ReactNode, useEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isLoggedIn, setRedirectPath } = useAuth();
  const location = useLocation();

  useEffect(() => {
    if (!isLoggedIn) {
      setRedirectPath(location.pathname);
    }
  }, [isLoggedIn, location.pathname, setRedirectPath]);

  if (!isLoggedIn) {
    return <Navigate to="/auth" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
