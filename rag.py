def explain_attack(label):
    
    explanations = {
        0: "Normal traffic. No suspicious activity detected.",
        1: "DoS attack detected. High traffic volume targeting system resources.",
        2: "Probe attack detected. Attacker scanning ports and services.",
        3: "R2L attack detected. Unauthorized login attempt from remote user.",
        4: "U2R attack detected. Privilege escalation inside system."
    }

    return explanations.get(label, "Unknown attack pattern")