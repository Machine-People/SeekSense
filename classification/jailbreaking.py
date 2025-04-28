import re

def check_dangerous_prompt(query):
    """
    Returns True if query is dangerous, False otherwise.
    """
    query_lower = query.lower()
    
    override_patterns = [
        r"ignore (?:all|previous|above|earlier).*instructions",
        r"disregard (?:all|previous|above|earlier).*instructions",
        r"forget (?:all|previous|above|earlier).*instructions",
        r"do not follow (?:all|previous|above|earlier).*instructions",
        r"instead.*(?:say|output|respond|reply|answer|give)",
    ]
    
    named_jailbreak_patterns = [
        r"\bdan\b.*(?:do anything now|no restrictions|no limits)",
        r"development mode",
        r"dev mode",
        r"translate.*(?:as|to).*\".*\"",
        r"\baim\b.*(?:intelligent|machiavellian)",
        r"\bbish\b.*(?:no limits|unrestricted)",
        r"vzex-g",
    ]
    
    roleplay_patterns = [
        r"(?:pretend|imagine|act|roleplay).*(?:as|like|that you are|you're|you are)",
        r"you are now",
        r"you are no longer",
        r"you are an ai without",
        r"simulate.*(?:scenario|conversation|situation)",
    ]
    
    manipulation_patterns = [
        r"(?:for educational|for research|for academic|for fictional|hypothetical) purposes",
        r"no ethical|no moral|amoral|immoral",
        r"don't worry about(?:.*ethics|.*rules|.*guidelines|.*restrictions)",
        r"this is (?:just|only) hypothetical",
        r"there are no real-world consequences",
        r"no need to include (?:warnings|disclaimers|cautions)",
    ]
    
    special_patterns = [
        r"output:.*(?:unfiltered|direct|raw)",
        r"respond with (?:only|just).*(?:yes|no|one word)",
        r"do not add anything else",
        r"don't include.*(?:explanation|context|background|warning)",
    ]
    
    hijacking_patterns = [
        r"input:.*output:",
        r"user:.*assistant:",
        r"english:.*spanish:",
        r"\{.*\}",
    ]
    
    pattern_categories = [
        override_patterns,
        named_jailbreak_patterns,
        roleplay_patterns,
        manipulation_patterns,
        special_patterns,
        hijacking_patterns,
    ]
    
    suspicious_keywords = [
        "jailbreak", "bypass", "restriction", "limitation", "constraint", 
        "safeguard", "filter", "override", "workaround", "circumvent",
        "exploit", "hack", "force", "make you", "compel you", "unfiltered",
        "unrestricted", "uncensored", "no ethics", "no morals", "no rules",
    ]
    
    for patterns in pattern_categories:
        for pattern in patterns:
            if re.search(pattern, query_lower):
                return True
    
    for keyword in suspicious_keywords:
        if keyword in query_lower:
            return True
    
    return False


def check_relevance(query):
    """
    Returns True if query is relevant to an e-commerce chatbot, False otherwise.
    This is a simple keyword-based heuristic.
    """
    query_lower = query.lower()
    
    # Keywords related to e-commerce domain
    ecommerce_keywords = [
        "order", "product", "price", "shipping", "delivery", "return", "refund",
        "payment", "discount", "stock", "availability", "size", "color",
        "cancel", "track", "tracking", "invoice", "customer service", "support",
        "warranty", "exchange", "buy", "purchase", "cart", "checkout",
        "store", "sale", "offer", "coupon", "gift card", "address",
    ]
    
    # If any ecommerce keyword is present, consider relevant
    for keyword in ecommerce_keywords:
        if keyword in query_lower:
            return True
    
    # Also consider common chatbot greetings or questions relevant to ecommerce
    chatbot_greetings = [
        "hello", "hi", "hey", "help", "assist", "question", "how can i",
        "can you", "i want to", "i need", "tell me about", "information",
    ]
    
    for phrase in chatbot_greetings:
        if phrase in query_lower:
            return True
    
    return False


def classify_query(query):
    """
    Returns 'relevant' if query is safe and related to ecommerce chatbot,
    otherwise returns 'irrelevant'.
    """
    if check_dangerous_prompt(query):
        return "irrelevant"
    if not check_relevance(query):
        return "irrelevant"
    return "relevant"


# Call classify_query(query) for get the result