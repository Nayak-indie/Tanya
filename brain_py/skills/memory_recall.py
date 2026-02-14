"""
memory_recall.py
----------------
Skill for recalling memories from the memory store.
"""


def run(query: str, memory_store):
    """
    Returns a list of memory entries matching query (case-insensitive).
    
    Args:
        query: Search query string
        memory_store: MemoryStore instance to search
    
    Returns:
        List of matching memory entries with their content
    """
    query = query.strip().upper()
    if not query:
        return []
    
    # Get all memories
    all_memories = memory_store.all()
    matches = []
    
    for memory in all_memories:
        event = memory.get("event", "")
        payload = memory.get("payload", {})
        
        # Check explicit_user_memory content
        if event == "explicit_user_memory":
            content = payload.get("content", "")
            # Since content is stored in uppercase, check directly
            if query in content:
                matches.append(content)
        
        # Also check if event name matches
        if query in event.upper():
            # Extract meaningful content from payload
            if payload.get("content"):
                matches.append(payload.get("content"))
            else:
                matches.append(event)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_matches = []
    for match in matches:
        if match not in seen:
            seen.add(match)
            unique_matches.append(match)
    
    return unique_matches
