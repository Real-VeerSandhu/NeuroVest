import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Plus, TrendingUp, TrendingDown, Eye, X } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Position {
  ticker: string;
  shares: number;
  currentPrice?: number;
  name?: string;
  change?: number;
  changePercent?: number;
}

const Portfolio = () => {
  const [positions, setPositions] = useState<Position[]>([]);
  const [watchlist, setWatchlist] = useState<string[]>([]);
  const [newTicker, setNewTicker] = useState("");
  const [newShares, setNewShares] = useState("");
  const [watchlistTicker, setWatchlistTicker] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchPortfolio();
    fetchWatchlist();
  }, []);

  const fetchPortfolio = async () => {
    try {
      // Mock data for now - replace with actual API call
      setPositions([
        { 
          ticker: "AAPL", 
          shares: 10, 
          currentPrice: 180.50, 
          name: "Apple Inc.",
          change: 2.30,
          changePercent: 1.29
        },
        { 
          ticker: "MSFT", 
          shares: 5, 
          currentPrice: 415.20, 
          name: "Microsoft Corp.",
          change: -1.80,
          changePercent: -0.43
        }
      ]);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch portfolio",
        variant: "destructive",
      });
    }
  };

  const fetchWatchlist = async () => {
    try {
      // Mock data for now - replace with actual API call
      setWatchlist(["GOOGL", "AMZN", "TSLA"]);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch watchlist",
        variant: "destructive",
      });
    }
  };

  const addPosition = async () => {
    if (!newTicker || !newShares) return;
    
    setLoading(true);
    try {
      // Mock API call - replace with actual implementation
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newPosition: Position = {
        ticker: newTicker.toUpperCase(),
        shares: parseInt(newShares),
        currentPrice: Math.random() * 500 + 50, // Mock price
        name: `${newTicker.toUpperCase()} Corp.`,
        change: (Math.random() - 0.5) * 10,
        changePercent: (Math.random() - 0.5) * 5
      };
      
      setPositions([...positions, newPosition]);
      setNewTicker("");
      setNewShares("");
      
      toast({
        title: "Success",
        description: `Added ${newShares} shares of ${newTicker.toUpperCase()}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add position",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const addToWatchlist = async () => {
    if (!watchlistTicker) return;
    
    try {
      const ticker = watchlistTicker.toUpperCase();
      if (!watchlist.includes(ticker)) {
        setWatchlist([...watchlist, ticker]);
        setWatchlistTicker("");
        toast({
          title: "Success",
          description: `Added ${ticker} to watchlist`,
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add to watchlist",
        variant: "destructive",
      });
    }
  };

  const removeFromWatchlist = (ticker: string) => {
    setWatchlist(watchlist.filter(t => t !== ticker));
    toast({
      title: "Removed",
      description: `${ticker} removed from watchlist`,
    });
  };

  const totalValue = positions.reduce((sum, pos) => sum + (pos.currentPrice || 0) * pos.shares, 0);
  const totalGainLoss = positions.reduce((sum, pos) => sum + ((pos.change || 0) * pos.shares), 0);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">Portfolio</h1>
        <div className="text-right">
          <div className="text-2xl font-bold text-foreground">
            ${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
          <div className={`flex items-center space-x-1 ${totalGainLoss >= 0 ? 'text-chart-gain' : 'text-chart-loss'}`}>
            {totalGainLoss >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
            <span className="font-medium">
              ${Math.abs(totalGainLoss).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>
        </div>
      </div>

      {/* Add Position */}
      <Card className="bg-gradient-card">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Plus className="h-5 w-5" />
            <span>Add Position</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <Input
              placeholder="Ticker Symbol (e.g., AAPL)"
              value={newTicker}
              onChange={(e) => setNewTicker(e.target.value.toUpperCase())}
              className="flex-1"
            />
            <Input
              type="number"
              placeholder="Shares"
              value={newShares}
              onChange={(e) => setNewShares(e.target.value)}
              className="w-full sm:w-32"
            />
            <Button onClick={addPosition} disabled={loading || !newTicker || !newShares}>
              {loading ? "Adding..." : "Add Position"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Positions */}
      <Card>
        <CardHeader>
          <CardTitle>Current Positions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {positions.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                No positions yet. Add your first position above.
              </div>
            ) : (
              positions.map((position, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold text-foreground">{position.ticker}</span>
                      <span className="text-sm text-muted-foreground">{position.name}</span>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {position.shares} shares @ ${position.currentPrice?.toFixed(2)}
                    </div>
                  </div>
                  <div className="text-right space-y-1">
                    <div className="font-semibold text-foreground">
                      ${((position.currentPrice || 0) * position.shares).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </div>
                    <div className={`text-sm flex items-center justify-end space-x-1 ${(position.change || 0) >= 0 ? 'text-chart-gain' : 'text-chart-loss'}`}>
                      {(position.change || 0) >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                      <span>
                        {position.changePercent?.toFixed(2)}% (${Math.abs(position.change || 0).toFixed(2)})
                      </span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Watchlist */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Eye className="h-5 w-5" />
            <span>Watchlist</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex gap-4">
              <Input
                placeholder="Add ticker to watchlist"
                value={watchlistTicker}
                onChange={(e) => setWatchlistTicker(e.target.value.toUpperCase())}
                className="flex-1"
              />
              <Button onClick={addToWatchlist} disabled={!watchlistTicker}>
                Add to Watchlist
              </Button>
            </div>
            
            <div className="flex flex-wrap gap-2">
              {watchlist.map((ticker) => (
                <Badge key={ticker} variant="secondary" className="flex items-center space-x-2 px-3 py-1">
                  <span>{ticker}</span>
                  <X 
                    className="h-3 w-3 cursor-pointer hover:text-destructive" 
                    onClick={() => removeFromWatchlist(ticker)}
                  />
                </Badge>
              ))}
              {watchlist.length === 0 && (
                <div className="text-muted-foreground text-sm">
                  No stocks in your watchlist yet.
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Portfolio;