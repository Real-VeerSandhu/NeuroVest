import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { TrendingUp, Shield, PieChart, Search, Target, BarChart3 } from "lucide-react";

const Landing = () => {
  const features = [
    {
      icon: PieChart,
      title: "Portfolio Management",
      description: "Track your investments and monitor performance with real-time data."
    },
    {
      icon: Search,
      title: "Stock Research",
      description: "Get comprehensive stock information and market insights."
    },
    {
      icon: Target,
      title: "Watchlist",
      description: "Keep track of stocks you're interested in for future investments."
    },
    {
      icon: BarChart3,
      title: "Performance Analytics",
      description: "Analyze your portfolio performance with detailed charts and metrics."
    },
    {
      icon: Shield,
      title: "Secure & Reliable",
      description: "Your financial data is protected with enterprise-grade security."
    },
    {
      icon: TrendingUp,
      title: "Real-time Updates",
      description: "Stay updated with live market data and price movements."
    }
  ];

  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="text-center space-y-8 py-12 animate-fade-in">
        <div className="space-y-4">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground leading-tight">
            Smart Investing
            <br />
            <span className="bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
              Made Simple
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Take control of your financial future with our comprehensive portfolio management platform. 
            Track investments, research stocks, and make informed decisions.
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/portfolio">
            <Button variant="hero" size="lg" className="w-full sm:w-auto">
              View Portfolio
            </Button>
          </Link>
          <Link to="/research">
            <Button variant="outline" size="lg" className="w-full sm:w-auto">
              Start Research
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Grid */}
      <section className="space-y-12 animate-slide-up">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold text-foreground">
            Everything You Need to Invest Smart
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Our platform provides all the tools and insights you need to build and manage a successful investment portfolio.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="bg-gradient-card border-border/50 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-6 space-y-4">
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-lg font-semibold text-foreground">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center bg-gradient-card rounded-2xl p-12 space-y-6 border border-border/50">
        <h2 className="text-3xl font-bold text-foreground">
          Ready to Start Your Investment Journey?
        </h2>
        <p className="text-lg text-muted-foreground max-w-xl mx-auto">
          Join thousands of investors who trust our platform to manage their portfolios and make informed investment decisions.
        </p>
        <Link to="/portfolio">
          <Button variant="hero" size="lg">
            Get Started Today
          </Button>
        </Link>
      </section>
    </div>
  );
};

export default Landing;