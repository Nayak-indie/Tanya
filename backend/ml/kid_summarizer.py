"""
AI News Summarizer - Story-style Explanations for Teens
Explains news like a fascinating story with history and opinions
"""
import re
import random
from typing import Dict, List

class StorySummarizer:
    """Explain news in story form - like telling a friend the full scoop"""
    
    # Context database for various topics
    TOPIC_CONTEXTS = {
        "iran_nuclear": {
            "history": """Let's go back. Iran was once ruled by a King called the Shah, backed by the United States. The US loved the Shah because Iran had huge oil reserves and was an ally against the Soviet Union. But regular Iranians hated him - he was dictatorial and kept all the wealth for himself while most people lived in poverty.

In 1979, everything changed. There was a massive revolution led by an exiled religious leader named Ayatollah Khomeini. The Shah fled Iran, and Iran became an Islamic Republic. The new government was deeply anti-American - they were furious the US had supported the Shah. In November 1979, Iranian students stormed the US Embassy in Tehran and held Americans hostage for 444 days. That's when US-Iran relations completely broke down.

For decades, Iran was isolated. Then in 2002, the world discovered Iran had been secretly building nuclear facilities underground. This became a huge international crisis. The concern? Iran claimed its nuclear program was for electricity and medicine, but enriched uranium can also make nuclear weapons.

In 2015, after years of negotiations, Iran signed a deal (JCPOA) with the US, UK, France, Germany, China, and Russia. Iran agreed to limit its nuclear activities, and in return, economic sanctions were lifted. Iran could sell oil again and access frozen bank accounts.

But in 2018, President Trump withdrew the US from the deal and reimposed harsh sanctions. Iran started enriching uranium again. Now in 2026, with a new US administration, they're trying to negotiate again - this time in Geneva.""",
            "topics": ["iran", "persia", "iranian", "tehran", "ayatollah", "nuclear", "uranium", "enrichment", "israel", "geneva", "tehran"]
        },
        "ai": {
            "history": """The concept of artificial intelligence dates back to the 1950s when a scientist named Alan Turing wondered if machines could think. For decades, AI was mostly science fiction - think of movies like The Terminator or Star Wars. But in recent years, something changed. In 2012, researchers discovered that feeding massive amounts of data into neural networks (computer brains inspired by human brains) could achieve incredible results. Image recognition, speech translation, and eventually, text generation became possible. The breakthrough moment came in 2022 when OpenAI released ChatGPT - suddenly, anyone could have a conversation with an AI that seemed almost human. Since then, the AI race has been on.""",
            "topics": ["AI", "artificial intelligence", "machine learning", "chatgpt", "openai", "google deepmind", "neural network"]
        },
        "stock_market": {
            "history": """The stock market has been around since the 1600s when Dutch traders started buying and selling shares of the Dutch East India Company - the world's first publicly traded company. The idea was simple: instead of one person funding an entire trading expedition, thousands of people could each own a small piece. If the company made money, everyone made money. In America, the New York Stock Exchange (NYSE) was founded in 1792 under a buttonwood tree in Manhattan. Today, the stock market is a massive digital marketplace where billions of dollars change hands every single day.""",
            "topics": ["stock market", "stocks", "shares", "trading", "wall street", "dow jones", "nasdaq", "SPY", "index fund"]
        },
        "tech_industry": {
            "history": """The modern tech industry really took off in the 1970s when two guys in a garage - Bill Gates and Paul Allen - started Microsoft, and Steve Jobs founded Apple in his parents' garage. Then came the internet in the 1990s, dot-com boom, and eventually smartphones in the 2000s. Today, the biggest companies in the world are tech companies: Apple, Microsoft, Google (Alphabet), Amazon, and Meta (Facebook). These companies shape how we live, communicate, work, and even think.""",
            "topics": ["tech", "silicon valley", "startup", "apple", "microsoft", "google", "amazon", "meta", "facebook", "tesla", "spacex"]
        },
        "politics": {
            "history": """Politics has existed since humans first lived in groups and needed to make decisions together. In ancient times, there were kings and emperors. Then, around 2,500 years ago, Greece invented democracy - meaning "rule by the people." Citizens would gather and vote on important issues. Rome had a similar system with senators. Over centuries, different systems evolved: monarchies, democracies, dictatorships, and communism. Today, most countries have some form of democracy where people vote for their leaders. But politics is messy - parties disagree, laws are debated, and change is often slow.""",
            "topics": ["election", "president", "congress", "senate", "democrat", "republican", "vote", "parliament", "prime minister", "law", "policy"]
        },
        "war": {
            "history": """War is as old as humanity itself. Early humans fought over resources and territory. In the ancient world, empires like Rome, Persia, and China built massive armies. The 20th century saw the most destructive wars in history: World War I (1914-1918) and World War II (1939-1945), which involved most of the world's countries and resulted in over 70 million deaths. After WWII, the US and Soviet Union became superpowers and fought indirectly through the Cold War. Today, most countries try to avoid war through diplomacy - talking and negotiating instead of fighting.""",
            "topics": ["war", "military", "army", "soldiers", "conflict", "ukraine", "russia", "battle", "troops", "invasion"]
        },
        "climate": {
            "history": """Earth's climate has always changed naturally - ice ages came and went. But in the late 1800s, scientists noticed something: burning coal and oil (fossil fuels) was adding carbon dioxide to the atmosphere, which traps heat like a blanket. This is called the Greenhouse Effect. In 1988, NASA scientist James Hansen testified to Congress that global warming was real and caused by humans. Since then, climate change has become one of the biggest issues of our time. In 2015, nearly 200 countries signed the Paris Agreement to limit warming. But we're still using a lot of fossil fuels, and the Earth keeps getting warmer.""",
            "topics": ["climate change", "global warming", "carbon", "greenhouse", "emissions", "fossil fuel", "paris agreement", "environment", "temperature"]
        },
        "economy": {
            "history": """Economics is the study of how people make, share, and spend money. For most of human history, people bartered - trading goods for goods. Then, around 3,000 years ago, money was invented. Paper money came from China around 1,000 years ago. The modern banking system evolved over centuries. In the 1930s, the Great Depression (a massive economic crash) taught governments that they needed to step in to help. Today, central banks (like the Federal Reserve in the US) control interest rates and print money to keep the economy stable. But inflation, recessions, and financial crises still happen.""",
            "topics": ["economy", "inflation", "recession", "federal reserve", "interest rate", "GDP", "bank", "money", "financial"]
        },
        "energy": {
            "history": """For most of history, humans used wood and coal for energy. The Industrial Revolution (1760-1840) saw steam engines powered by coal transform factories and transportation. Then in the late 1800s, oil was discovered, leading to cars, planes, and modern life as we know it. But burning fossil fuels causes pollution and climate change. The solution? Clean energy! Solar power was first used in the 1950s, wind turbines in the 1970s. Today, solar and wind are the fastest-growing energy sources. Electric cars are becoming common. The energy transition is happening - but it's slow and complicated.""",
            "topics": ["energy", "solar", "wind", "oil", "gas", "electric", "renewable", "coal", "OPEC", "electric vehicle", "EV", "battery"]
        },
        "health": {
            "history": """Modern medicine has come incredibly far. In the 1800s, doctors didn't wash their hands (gross!), leading to many deaths from infections. Then in 1928, Alexander Fleming discovered penicillin - the first antibiotic - by accident when he noticed mold killing bacteria in a petri dish. In the 1950s, vaccines virtually eliminated diseases like polio. In 2003, scientists mapped the entire human genome. In 2020, COVID-19 emerged, and scientists created vaccines in record time using mRNA technology. Today, we're working on curing cancer, AI-assisted diagnosis, and personalized medicine tailored to your DNA.""",
            "topics": ["health", "virus", "vaccine", "covid", "pandemic", "doctor", "hospital", "medicine", "drug", "pharma", "Pfizer", "Moderna"]
        },
        "space": {
            "history": """Humans have always looked at the stars and wondered. But space exploration only began in 1957 when the Soviet Union launched Sputnik - the first satellite. In 1961, Yuri Gagarin became the first human in space. In 1969, American astronauts walked on the Moon - the Apollo 11 mission. After that, space agencies built space stations where astronauts live for months. In recent years, private companies like SpaceX (founded by Elon Musk) have revolutionized space travel by making rockets reusable. Now, there's a race to send humans to Mars, and companies are planning space tourism for wealthy adventurers.""",
            "topics": ["space", "nasa", "moon", "mars", "rocket", "spacex", "astronaut", "satellite", "launch", "space station", "iss"]
        }
    }
    
    def detect_topic(self, title: str, summary: str) -> str:
        """Detect which topic this news is about"""
        text = (title + " " + summary).lower()
        
        # Check for Iran first (more specific)
        if any(kw in text for kw in ["iran", "iranian", "tehran", "persia", "ayatollah"]):
            return "iran_nuclear"
        
        scores = {}
        for topic, data in self.TOPIC_CONTEXTS.items():
            score = 0
            for keyword in data["topics"]:
                if keyword.lower() in text:
                    score += 1
            if score > 0:
                scores[topic] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "general"
    
    def generate_summary(self, title: str, summary: str = "") -> Dict:
        """Generate a story-style summary with history and opinion"""
        
        # Detect topic
        topic = self.detect_topic(title, summary)
        
        # Get context
        topic_data = self.TOPIC_CONTEXTS.get(topic, {})
        history = topic_data.get("history", self._generate_general_history(title, summary))
        
        # Generate current situation
        current = self._generate_current_situation(title, summary, topic)
        
        # Generate opinion/conclusion
        opinion = self._generate_opinion(title, summary, topic)
        
        return {
            "title": title,
            "history": history,
            "current": current,
            "opinion": opinion,
            "topic": topic
        }
    
    def _generate_general_history(self, title: str, summary: str) -> str:
        """Generate history for unknown topics"""
        return f"""Every news story has a background, and this one is no different. The topic of "{title}" has been developing over time, shaped by events, decisions, and people who came before. To understand what's happening now, it helps to know how we got here.

This particular issue has been in the making for years, sometimes decades. It involves complex systems, institutions, and interests that have evolved over time. What you're seeing in the news today is just the latest chapter in an ongoing story."""
    
    def _generate_current_situation(self, title: str, summary: str, topic: str) -> str:
        """Explain what's happening now"""
        # Extract entities
        numbers = re.findall(r'\d+%|\$\d+\s*(billion|million)|[\d,]+(?=\s*(people|users|customers))', summary)
        countries = re.findall(r'(United States|China|Russia|India|UK|Japan|Germany|France|Brazil|Israel|Ukraine|Saudi Arabia)', summary)
        
        current = f"""Now let's talk about what's happening right now. {title.replace('.', '')} is making headlines because """
        
        # Add extracted info
        if countries:
            current += f"{countries[0]} "
        
        if numbers:
            current += f"with {numbers[0]} "
        
        # Add topic-specific current situation
        topic_situations = {
            "iran_nuclear": f"""US and Iranian diplomats are meeting in Geneva, Switzerland for new nuclear talks. This is significant because direct US-Iran negotiations are rare - they usually happen through intermediaries.

What's on the table? The US wants Iran to stop enriching uranium to levels that could be used for weapons. Iran wants all economic sanctions lifted so their economy can recover. Iran currently has about 60% enrichment, which is far beyond what civilian nuclear power needs but below the 90% threshold for a bomb.

China, Russia, France, Germany, and the UK are also involved in these talks. Everyone wants to prevent Iran from acquiring nuclear weapons - but they disagree on how to get there.

Israel, Iran's arch-enemy, is watching very nervously. Israel has warned it won't allow Iran to get nuclear weapons and has carried out sabotage attacks on Iranian nuclear facilities in the past.

The stakes are huge. If they reach a deal, it could bring stability to the Middle East. If talks fail, Iran might enrich to weapons-grade, Israel might strike militarily.""",
            
            "ai": f"""The AI world is exploding with developments. Companies are racing to build more powerful AI systems, and everyone wants to be the leader. There's excitement about what AI can do - from writing code to creating art - but also serious concerns about job displacement, misinformation, and whether AI might become too powerful. Governments are scrambling to create regulations.""",
            
            "stock_market": f"""The market has been going through interesting times. There are debates about whether we're heading into a recession, if tech stocks are overvalued, and what the Federal Reserve will do with interest rates. Some investors are optimistic, others are cautious. The ongoing AI boom has been driving a lot of the growth.""",
            
            "tech_industry": f"""Big Tech is facing more scrutiny than ever. Regulators are worried about monopolies and data privacy. Apple, Google, Meta, and Amazon are constantly in the news - whether it's new product launches, antitrust lawsuits, or layoffs. The AI push has made tech stocks volatile but also incredibly valuable.""",
            
            "politics": f"""Politics is as polarized as ever. There are intense debates about the economy, immigration, healthcare, and foreign policy. Upcoming elections are on everyone's mind. Politicians are campaigning, making promises, and attacking each other.""",
            
            "war": f"""Conflict continues to devastate civilians while world leaders argue about what to do. Military aid, sanctions, and diplomatic negotiations are ongoing. There's debate about whether to support one side or stay neutral. The human cost is enormous.""",
            
            "climate": f"""Climate change is accelerating faster than expected. Extreme weather events are becoming more frequent - floods, wildfires, heatwaves. There's pressure on governments and companies to act faster. Some countries are leading the charge with clean energy.""",
            
            "economy": f"""The economic outlook is mixed. Inflation has cooled but remains a concern. Central banks are walking a tightrope - raising rates too much could cause a recession, not raising enough might let inflation spiral. Job markets are showing signs of weakening.""",
            
            "energy": f"""The energy world is undergoing a massive transformation. Solar and wind are now the cheapest sources of new electricity in most places. Electric cars are going mainstream. But there's still resistance from fossil fuel companies.""",
            
            "health": f"""Post-pandemic, healthcare is still recovering. There's debate about vaccine policies, healthcare costs, and the healthcare worker shortage. Mental health is getting more attention. AI is being integrated into diagnostics.""",
            
            "space": f"""Space is getting more crowded and competitive. NASA is planning to return to the Moon. SpaceX is launching satellites and planning Mars missions. Private companies are building space stations. Space tourism might become reality."""
        }
        
        current += topic_situations.get(topic, "this is an evolving situation that people are closely watching.")
        
        return current
    
    def _generate_opinion(self, title: str, summary: str, topic: str) -> str:
        """Generate balanced opinion/conclusion"""
        
        opinions = {
            "iran_nuclear": """Alright, here's my take on these talks. Iran is a complicated situation. On one hand, Iran has every right to nuclear energy - plenty of countries have nuclear power plants. But here's the thing: enriching uranium to 60-90% is a different ballgame. That's weapons-grade territory. Iran's nuclear sites are hidden underground, they've blocked inspectors, and they've enriched faster than anyone expected after the US left the deal.

The sanctions really suck for ordinary Iranians - they can't buy medicine, cars, or pretty much anything from the West. But does the Iranian government care? They still fund Hezbollah in Lebanon, Houthis in Yemen, and Hamas in Palestine. So it's complicated.

My honest opinion? A deal is absolutely better than war. A US-Iran war would be an absolute catastrophe - Iran isn't Iraq or Afghanistan, it's a big country with proxies across the Middle East, and China and Russia would likely back them. Oil prices would skyrocket and the global economy would tank.

But any deal needs real verification. Iran has a history of cheating - they hid nuclear sites from inspectors for years. So trust but verify. Also, Israel is a wild card here - they've sabotaged Iran's program before and they might not wait for diplomacy.

Bottom line: these talks matter. A lot. Let's hope they find middle ground.""",
            
            "ai": """So what should we think about all this? AI is genuinely transformative - it's not just hype. The technology behind ChatGPT and image generators is remarkable, and it'll likely change how we work and live. But there are real concerns: job displacement, misinformation, algorithmic bias, and the question of whether AI systems can be trusted. The key is to be excited about the possibilities while staying skeptical of the hype. Not everything AI companies claim is true, and not every use case makes sense. The best approach: learn about it, form your own opinions, and remember that technology amplifies both human capability and human folly.""",
            
            "stock_market": """What does this mean for regular people? The stock market can feel abstract - it's all numbers and algorithms. But it affects your 401(k), your job, and the prices you pay. The truth is, trying to time the market is nearly impossible. History shows that staying invested for the long term beats trying to guess the next big move. That said, be skeptical of anyone claiming to have figured out what the market will do next. Diversification, patience, and not investing money you can't afford to lose are the boring but wise strategies.""",
            
            "tech_industry": """Big Tech companies have given us incredible products - smartphones, search engines, streaming, online shopping. But their size and power raise valid concerns about competition, privacy, and democracy. The next decade will determine whether tech remains a force for good or becomes more problematic. As users, we have power - our choices, our data, and our attention shape what companies do. Stay informed, read the fine print, and don't assume anything is truly "free." """,
            
            "politics": """Here's the uncomfortable truth: politics affects everything, but it's also incredibly frustrating. Politicians promise a lot and often deliver less. Partisanship makes compromise difficult. But ignoring politics doesn't make it go away - it just means other people make decisions for you. The best approach: learn about the issues, understand different perspectives (even if you disagree), vote, and stay engaged. Change is slow, but it happens. The world today is vastly different from 50 years ago - in both good and bad ways.""",
            
            "war": """War is hell, and it's important to remember that behind every statistic are real people - families displaced, children traumatized, communities destroyed. It's easy to get caught up in geopolitics and forget the human cost. That said, complex situations sometimes don't have good options - only less bad ones. The best any of us can do is stay informed, advocate for peace, and remember that our taxes fund militaries. Peace isn't just the absence of war - it requires constant effort.""",
            
            "climate": """Climate change is the defining issue of our time. It's not a future problem - it's happening now. The good news: clean energy is becoming cheaper, technology is improving, and younger generations care deeply. The bad news: we're not acting fast enough, and the fossil fuel industry has enormous political power. What can you do? Stay informed, make sustainable choices when possible, and support leaders who take this seriously. Individual actions matter, but systemic change matters more.""",
            
            "economy": """The economy affects everyone, but it's notoriously difficult to predict. Economists constantly disagree, and the economy often confects expectations. The best financial advice is timeless: live within your means, save for emergencies, invest for the long term, and don't make decisions based on fear or greed. Economic crises will happen - they always have. What matters is being prepared and staying calm.""",
            
            "energy": """The energy transition is happening, whether certain politicians and companies like it or not. Solar and wind are now cheaper than fossil fuels in most cases. Electric cars are becoming mainstream. The jobs of the future are in clean energy. But the transition won't be smooth - there will be winners and losers, and certain industries and regions will struggle. The key is to support workers through the transition and not let perfect be the enemy of good. Every percentage of clean energy we add makes a difference.""",
            
            "health": """Health is personal - what works for one person might not work for another. The pandemic taught us that public health requires collective action. We learned that viruses don't respect borders and that science is messy - it evolves as we learn more. The best approach: stay informed but don't panic, trust credible experts (but verify), and take care of your physical and mental health. The healthcare system has problems, but also remarkable innovations are happening.""",
            
            "space": """Space is the ultimate frontier, and there's something uniquely inspiring about exploring it. But space isn't just for scientists and billionaires - it's becoming an industry. Satellite internet, Earth observation, and one day, space tourism and mining could affect all of us. The question is: should we prioritize space exploration when we have problems on Earth? Many argue that solving Earth's problems first is more important. Others say innovation in space can help solve Earth problems. Either way, space is becoming more accessible, and this is just the beginning."""
        }
        
        return opinions.get(topic, """Every news story has multiple perspectives, and the truth is often more nuanced than headlines suggest. The best approach is to stay informed from multiple sources, question assumptions (including your own), and remember that complex issues rarely have simple answers. What matters is forming your own opinion based on evidence, not just emotion or ideology.""")
    
    def generate_full_story(self, title: str, summary: str = "") -> str:
        """Generate complete story for display"""
        result = self.generate_summary(title, summary)
        
        story = f"""# {title}

## 📜 The Backstory - How We Got Here

{result['history']}

---

## 🔥 What's Happening Right Now

{result['current']}

---

## 💭 My Take - A Balanced Perspective

{result['opinion']}

---

*The goal here isn't to tell you what to think, but to give you enough context to form your own opinions. News literacy matters - question everything, seek multiple perspectives, and remember that every story has more to it than meets the eye.*

---
*Topic: {result['topic'].replace('_', ' ').title()}*
"""
        return story


# Example usage
if __name__ == "__main__":
    summarizer = StorySummarizer()
    
    # Test with sample news
    test_title = "AI Companies Race to Build More Powerful Systems"
    test_summary = "OpenAI, Google, and Microsoft are competing to develop the most advanced AI systems. The competition has intensified following the success of ChatGPT. Experts warn about potential risks."
    
    story = summarizer.generate_full_story(test_title, test_summary)
    print(story)
