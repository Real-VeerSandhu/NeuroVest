import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { TrendingUp, Briefcase, Search, User, LogIn } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

const AppTitle: string = "NeuroVest"

const Navigation = () => {
  const location = useLocation();
  const { isLoggedIn } = useAuth();

  const navItems = [
    { href: "/", label: "Home", icon: TrendingUp, requiresAuth: false },
    { href: "/portfolio", label: "Portfolio", icon: Briefcase, requiresAuth: true },
    { href: "/research", label: "Research", icon: Search, requiresAuth: true },
  ];

  return (
    <nav className="bg-card/95 border-b border-border sticky top-0 z-50 backdrop-blur-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <TrendingUp className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold text-foreground">{AppTitle}</span>
          </Link>
          
          <div className="flex items-center space-x-1">
            {navItems
              .filter((item) => !item.requiresAuth || isLoggedIn)
              .map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;
                
                return (
                  <Link key={item.href} to={item.href}>
                    <Button
                      variant={isActive ? "default" : "ghost"}
                      size="sm"
                      className="flex items-center space-x-2"
                    >
                      <Icon className="h-4 w-4" />
                      <span className="hidden sm:inline">{item.label}</span>
                    </Button>
                  </Link>
                );
              })}
            
            {isLoggedIn ? (
              <Link to="/account" className="ml-4">
                <Button
                  variant="ghost"
                  size="sm"
                  className="flex items-center space-x-2"
                >
                  <User className="h-4 w-4" />
                  <span className="hidden sm:inline">Account</span>
                </Button>
              </Link>
            ) : (
              <Link to="/auth" className="ml-4">
                <Button
                  variant="default"
                  size="sm"
                  className="flex items-center space-x-2"
                >
                  <LogIn className="h-4 w-4" />
                  <span className="hidden sm:inline">Login</span>
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;