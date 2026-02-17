# Tanya RSS Fetcher in Elixir
# Run: mix run elixir/rss_fetcher.exs
# Requires: Mix project setup

defmodule Tanya.RSSFetcher do
  @moduledoc """
  RSS Feed Fetcher - Elixir implementation
  """

  @feeds [
    %{name: "BBC", url: "http://feeds.bbci.co.uk/news/world/rss.xml", category: "World"},
    %{name: "TechCrunch", url: "https://techcrunch.com/feed/", category: "Tech"},
  ]

  @doc """
  Fetch RSS from URL
  """
  def fetch(url) do
    case HTTPoison.get(url, [{"User-Agent", "Tanya/1.0 (Elixir)"}]) do
      {:ok, %HTTPoison.Response{status_code: 200, body: body}} ->
        {:ok, body}
      {:error, reason} ->
        {:error, reason}
    end
  end

  @doc """
  Parse RSS XML
  """
  def parse(xml) do
    items = []
    
    # Extract titles (simplified)
    titles = Regex.scan(~r/<title>([^<]+)<\/title>/, xml, capture: :all)
              |> Enum.map(fn [_, title] -> title end)
              |> Enum.drop(1)  # Drop channel title
    
    Enum.map(titles, fn title ->
      %{
        title: title,
        sentiment: analyze_sentiment(title),
        category: infer_category(title),
        source: "Elixir"
      }
    end)
  end

  @doc """
  Simple sentiment analysis
  """
  def analyze_sentiment(text) do
    text = String.downcase(text)
    
    positive = ~w(good great excellent amazing breakthrough success win)
    negative = ~w(bad terrible crisis fail death war attack disaster)
    
    pos_count = Enum.count(positive, &String.contains?(text, &1))
    neg_count = Enum.count(negative, &String.contains?(text, &1))
    
    cond do
      pos_count > neg_count -> "positive"
      neg_count > pos_count -> "negative"
      true -> "neutral"
    end
  end

  @doc """
  Infer category from title
  """
  def infer_category(title) do
    text = String.downcase(title)
    
    cond do
      String.contains?(text, "ai") or String.contains?(text, "artificial intelligence") -> "AI"
      String.contains?(text, "tech") or String.contains?(text, "software") -> "Tech"
      String.contains?(text, "stock") or String.contains?(text, "market") -> "Finance"
      String.contains?(text, "war") or String.contains?(text, "military") -> "World"
      String.contains?(text, "science") or String.contains?(text, "space") -> "Science"
      true -> "General"
    end
  end

  @doc """
  Main runner
  """
  def run(args \\ []) do
    IO.puts("Tanya RSS Fetcher (Elixir)")
    IO.puts("===========================")
    IO.puts("")

    feeds = if "--url" in args do
      idx = Enum.find_index(args, &(&1 == "--url"))
      if idx && Enum.at(args, idx + 1) do
        [%{name: "Custom", url: Enum.at(args, idx + 1), category: "General"}]
      else
        @feeds
      end
    else
      @feeds
    end

    all_items = []
    
    for feed <- feeds do
      IO.puts("Fetching #{feed.name}...")
      
      case fetch(feed.url) do
        {:ok, xml} ->
          items = parse(xml)
          IO.puts("  -> Found #{length(items)} articles")
          Enum.each(items, fn item ->
            IO.puts("    - #{item.title}")
          end)
          all_items = items ++ all_items
          
        {:error, reason} ->
          IO.puts("  -> Error: #{reason}")
      end
    end
    
    IO.puts("")
    IO.puts("Total: #{length(all_items)} articles")
    IO.puts("Engine: Elixir (fault-tolerant, distributed)")
  end
end

# If run directly
if System.get_env("MIX_ENV") == nil || true do
  Tanya.RSSFetcher.run(System.argv())
end
