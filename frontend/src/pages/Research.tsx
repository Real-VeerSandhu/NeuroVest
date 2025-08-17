import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, TrendingUp, TrendingDown, Building2, DollarSign } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface StockInfo {
  ticker: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  marketCap: number;
  sector: string;
  volume: number;
  high52w: number;
  low52w: number;
  pe: number;
}

const Research = () => {
  const [searchTicker, setSearchTicker] = useState("");
  const [stockInfo, setStockInfo] = useState<StockInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const searchStock = async () => {
    if (!searchTicker) return;
    
    setLoading(true);
    try {
      // Mock API call - replace with actual implementation
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock stock data
      const mockStock: StockInfo = {
        ticker: searchTicker.toUpperCase(),
        name: `${searchTicker.toUpperCase()} Corporation`,
        price: Math.random() * 500 + 50,
        change: (Math.random() - 0.5) * 20,
        changePercent: (Math.random() - 0.5) * 5,
        marketCap: Math.random() * 1000000000000 + 10000000000,
        sector: ["Technology", "Healthcare", "Financial", "Consumer", "Energy"][Math.floor(Math.random() * 5)],
        volume: Math.random() * 10000000 + 1000000,
        high52w: Math.random() * 600 + 100,
        low52w: Math.random() * 100 + 20,
        pe: Math.random() * 30 + 5
      };
      
      setStockInfo(mockStock);
      toast({
        title: "Stock Found",
        description: `Retrieved information for ${searchTicker.toUpperCase()}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch stock information",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const formatMarketCap = (value: number) => {
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
    return `$${value.toLocaleString()}`;
  };

  const formatVolume = (value: number) => {
    if (value >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(2)}K`;
    return value.toLocaleString();
  };

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold text-foreground">Stock Research</h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Search for stocks and get comprehensive information including current price, market cap, sector details, and key financial metrics.
        </p>
      </div>

      {/* Search */}
      <Card className="bg-gradient-card">
        <CardContent className="p-6">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Enter stock ticker (e.g., AAPL, MSFT, GOOGL)"
                value={searchTicker}
                onChange={(e) => setSearchTicker(e.target.value.toUpperCase())}
                className="pl-10"
                onKeyPress={(e) => e.key === 'Enter' && searchStock()}
              />
            </div>
            <Button onClick={searchStock} disabled={loading || !searchTicker}>
              {loading ? "Searching..." : "Search"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Stock Information */}
      {stockInfo && (
        <div className="space-y-6 animate-fade-in">
          {/* Stock Header */}
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
                <div className="space-y-2">
                  <div className="flex items-center space-x-3">
                    <h2 className="text-2xl font-bold text-foreground">{stockInfo.ticker}</h2>
                    <Badge variant="secondary" className="flex items-center space-x-1">
                      <Building2 className="h-3 w-3" />
                      <span>{stockInfo.sector}</span>
                    </Badge>
                  </div>
                  <p className="text-muted-foreground">{stockInfo.name}</p>
                </div>
                
                <div className="text-right space-y-1">
                  <div className="text-3xl font-bold text-foreground">
                    ${stockInfo.price.toFixed(2)}
                  </div>
                  <div className={`flex items-center justify-end space-x-1 text-lg ${stockInfo.change >= 0 ? 'text-chart-gain' : 'text-chart-loss'}`}>
                    {stockInfo.change >= 0 ? <TrendingUp className="h-5 w-5" /> : <TrendingDown className="h-5 w-5" />}
                    <span>
                      {stockInfo.changePercent >= 0 ? '+' : ''}{stockInfo.changePercent.toFixed(2)}% 
                      (${stockInfo.change >= 0 ? '+' : ''}{stockInfo.change.toFixed(2)})
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center space-x-2">
                  <DollarSign className="h-4 w-4" />
                  <span>Market Cap</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-2xl font-bold text-foreground">
                  {formatMarketCap(stockInfo.marketCap)}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground">Volume</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-2xl font-bold text-foreground">
                  {formatVolume(stockInfo.volume)}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground">P/E Ratio</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-2xl font-bold text-foreground">
                  {stockInfo.pe.toFixed(2)}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground">52W High</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-2xl font-bold text-foreground">
                  ${stockInfo.high52w.toFixed(2)}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground">52W Low</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-2xl font-bold text-foreground">
                  ${stockInfo.low52w.toFixed(2)}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground">Sector</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-2xl font-bold text-foreground">
                  {stockInfo.sector}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* No Search Results */}
      {!stockInfo && !loading && (
        <Card className="border-dashed border-2">
          <CardContent className="p-12 text-center space-y-4">
            <Search className="h-12 w-12 text-muted-foreground mx-auto" />
            <div className="space-y-2">
              <h3 className="text-lg font-semibold text-foreground">No Stock Selected</h3>
              <p className="text-muted-foreground">
                Enter a stock ticker symbol above to get comprehensive stock information and analysis.
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Research;