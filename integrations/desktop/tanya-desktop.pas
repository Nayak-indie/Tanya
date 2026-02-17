program TanyaDesktop;

{$APPTYPE CONSOLE}

uses
  SysUtils, Classes, DateUtils, Math;

type
  TArticle = record
    ID: string;
    Title: string;
    Link: string;
    Content: string;
    Published: TDateTime;
    Sentiment: string;
    ReadingTime: Integer;
  end;

  TArticleArray = array of TArticle;

{ Calculate reading time in minutes }
function CalculateReadingTime(const Content: string): Integer;
var
  WordCount, WPM: Integer;
begin
  WordCount := 0;
  WPM := 200; // Words per minute

  // Simple word counting
  var I := 1;
  var InWord := False;

  while I <= Length(Content) do
  begin
    if Content[I] in ['A'..'Z', 'a'..'z', '0'..'9'] then
    begin
      if not InWord then
      begin
        InWord := True;
        Inc(WordCount);
      end;
    end
    else
      InWord := False;
    Inc(I);
  end;

  Result := Max(1, Ceil(WordCount / WPM));
end;

{ Simple sentiment analysis }
function AnalyzeSentiment(const Text: string): string;
var
  Words: TStringList;
  I, Score: Integer;
begin
  Words := TStringList.Create;
  try
    Words.DelimitedText := Text;
    Words.Delimiter := ' ';
    Score := 0;

    for I := 0 to Words.Count - 1 do
    begin
      var Word := LowerCase(Words[I]);

      if (Word = 'good') or (Word = 'great') or (Word = 'excellent') or
         (Word = 'amazing') or (Word = 'success') or (Word = 'breakthrough') then
        Inc(Score, 2)
      else if (Word = 'bad') or (Word = 'terrible') or (Word = 'horrible') or
              (Word = 'failure') or (Word = 'crisis') or (Word = 'disaster') then
        Dec(Score, 2);
    end;

    if Score > 0 then
      Result := 'positive'
    else if Score < 0 then
      Result := 'negative'
    else
      Result := 'neutral';
  finally
    Words.Free;
  end;
end;

{ Export articles to CSV }
procedure ExportToCSV(const Articles: TArticleArray; const FileName: string);
var
  F: TextFile;
  I: Integer;
begin
  AssignFile(F, FileName);
  try
    Rewrite(F);
    WriteLn(F, 'ID,Title,Link,Published,Sentiment,Reading Time');

    for I := Low(Articles) to High(Articles) do
    begin
      WriteLn(F, Format('%s,"%s","%s","%s",%s,%d',
        [Articles[I].ID,
         Articles[I].Title,
         Articles[I].Link,
         DateTimeToStr(Articles[I].Published),
         Articles[I].Sentiment,
         Articles[I].ReadingTime]));
    end;
  finally
    CloseFile(F);
  end;

  WriteLn(Format('Exported %d articles to %s', [Length(Articles), FileName]));
end;

{ Filter articles by sentiment }
function FilterBySentiment(const Articles: TArticleArray;
  const Sentiment: string): TArticleArray;
var
  I, J: Integer;
begin
  SetLength(Result, 0);
  J := 0;

  for I := Low(Articles) to High(Articles) do
  begin
    if Articles[I].Sentiment = Sentiment then
    begin
      SetLength(Result, J + 1);
      Result[J] := Articles[I];
      Inc(J);
    end;
  end;
end;

{ Find duplicates based on title similarity }
function FindDuplicates(const Articles: TArticleArray;
  Threshold: Double = 0.8): TArray<TPair<string, string>>;
var
  I, J: Integer;
  Similarity: Double;
begin
  SetLength(Result, 0);
  var Count := 0;

  for I := Low(Articles) to High(Articles) do
    for J := I + 1 to High(Articles) do
    begin
      // Simple similarity check (same words)
      var Words1 := Articles[I].Title.Split([' ', ',', '.']);
      var Words2 := Articles[J].Title.Split([' ', ',', '.']);
      var MatchCount := 0;

      for var W1 in Words1 do
        for var W2 in Words2 do
          if SameText(W1, W2) then
            Inc(MatchCount);

      if (Length(Words1) > 0) and (Length(Words2) > 0) then
        Similarity := MatchCount / Max(Length(Words1), Length(Words2))
      else
        Similarity := 0;

      if Similarity >= Threshold then
      begin
        SetLength(Result, Count + 1);
        Result[Count].Key := Articles[I].ID;
        Result[Count].Value := Articles[J].ID;
        Inc(Count);
      end;
    end;
end;

var
  SampleArticles: TArticleArray;
  Filtered: TArticleArray;
  Duplicates: TArray<TPair<string, string>>;
  I: Integer;

begin
  WriteLn('Tanya Desktop Module (Delphi/Object Pascal)');
  WriteLn('============================================');

  // Sample data
  SetLength(SampleArticles, 3);
  SampleArticles[0].ID := '1';
  SampleArticles[0].Title := 'AI Breakthrough Announced';
  SampleArticles[0].Link := 'https://example.com/1';
  SampleArticles[0].Content := 'Great success in artificial intelligence research';
  SampleArticles[0].Published := Now;
  SampleArticles[0].Sentiment := 'neutral';
  SampleArticles[0].ReadingTime := 0;

  SampleArticles[1].ID := '2';
  SampleArticles[1].Title := 'Market Crash Warning';
  SampleArticles[1].Link := 'https://example.com/2';
  SampleArticles[1].Content := 'Terrible news for investors as markets fall';
  SampleArticles[1].Published := Now;
  SampleArticles[1].Sentiment := 'neutral';
  SampleArticles[1].ReadingTime := 0;

  SampleArticles[2].ID := '3';
  SampleArticles[2].Title := 'AI Update Released';
  SampleArticles[2].Link := 'https://example.com/3';
  SampleArticles[2].Content := 'New AI features announced';
  SampleArticles[2].Published := Now;
  SampleArticles[2].Sentiment := 'neutral';
  SampleArticles[2].ReadingTime := 0;

  // Process articles
  for I := Low(SampleArticles) to High(SampleArticles) do
  begin
    SampleArticles[I].Sentiment := AnalyzeSentiment(SampleArticles[I].Content);
    SampleArticles[I].ReadingTime := CalculateReadingTime(SampleArticles[I].Content);
    WriteLn(Format('Article %d: %s (%d min, %s)',
      [I + 1, SampleArticles[I].Title,
       SampleArticles[I].ReadingTime,
       SampleArticles[I].Sentiment]));
  end;

  // Find duplicates
  Duplicates := FindDuplicates(SampleArticles, 0.5);
  WriteLn(Format('Found %d duplicate pairs', [Length(Duplicates)]));

  // Export to CSV
  ExportToCSV(SampleArticles, 'articles.csv');

  WriteLn('Done!');
end.
