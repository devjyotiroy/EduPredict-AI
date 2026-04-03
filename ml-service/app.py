from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, mean_squared_error
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load saved models
performance_model = joblib.load("performance_model.pkl")
career_model = joblib.load("career_model.pkl")
interest_encoder = joblib.load("interest_encoder.pkl")
career_encoder = joblib.load("career_encoder.pkl")


# -------------------------------------------------
# Performance Category Function
# -------------------------------------------------
def get_performance_category(marks):
    if marks >= 85:
        return "Excellent"
    elif marks >= 70:
        return "Good"
    elif marks >= 50:
        return "Average"
    else:
        return "Needs Improvement"

# -------------------------------------------------
# Weak Area Detection
# -------------------------------------------------
def detect_weak_areas(study_hours, attendance, previous_marks, programming_skill, communication_skill):
    weak_areas = []
    
    if study_hours < 3:
        weak_areas.append("Study Hours")
    if attendance < 75:
        weak_areas.append("Attendance")
    if previous_marks < 60:
        weak_areas.append("Previous Performance")
    if programming_skill < 2:
        weak_areas.append("Programming Skills")
    if communication_skill < 2:
        weak_areas.append("Communication Skills")
    
    return weak_areas

# -------------------------------------------------
# Improvement Recommendations
# -------------------------------------------------
def get_recommendations(weak_areas, predicted_marks):
    recommendations = []
    
    if "Study Hours" in weak_areas:
        recommendations.append("Increase daily study hours to at least 4-5 hours")
    if "Attendance" in weak_areas:
        recommendations.append("Improve attendance to above 80%")
    if "Previous Performance" in weak_areas:
        recommendations.append("Focus on understanding core concepts and practice regularly")
    if "Programming Skills" in weak_areas:
        recommendations.append("Practice coding on platforms like LeetCode, HackerRank")
    if "Communication Skills" in weak_areas:
        recommendations.append("Join speaking clubs or practice presentations")
    
    if predicted_marks < 70:
        recommendations.append("Consider taking extra tutoring sessions")
        recommendations.append("Create a structured study schedule")
    
    return recommendations


# -------------------------------------------------
# Career Roadmap Generator
# -------------------------------------------------
def generate_career_roadmap(career):
    roadmaps = {
        "Software Engineer": [
            "Month 1-3: Master Data Structures & Algorithms",
            "Month 4-6: Learn Web Development (HTML, CSS, JavaScript, React)",
            "Month 7-9: Backend Development (Node.js, Python, Databases)",
            "Month 10-12: Build 3-5 Full Stack Projects",
            "Year 2: Learn System Design, Cloud (AWS/Azure), DevOps",
            "Year 3: Contribute to Open Source, Prepare for Interviews"
        ],
        "Android Developer": [
            "Month 1-3: Master Java/Kotlin, Android Studio Basics",
            "Month 4-6: Learn Android UI/UX, Material Design",
            "Month 7-9: APIs, Firebase, Database (Room, SQLite)",
            "Month 10-12: Build 3-5 Android Apps, Publish on Play Store",
            "Year 2: Advanced Topics (MVVM, Jetpack Compose, Testing)",
            "Year 3: Learn Cross-platform (Flutter/React Native), Portfolio"
        ],
        "Mobile Developer": [
            "Month 1-3: Choose Platform (Android/iOS), Learn Basics",
            "Month 4-6: UI Development, Navigation, State Management",
            "Month 7-9: APIs, Backend Integration, Local Storage",
            "Month 10-12: Build Mobile Apps, App Store Deployment",
            "Year 2: Cross-platform Development (Flutter/React Native)",
            "Year 3: Advanced Features, Performance Optimization"
        ],
        "Data Scientist": [
            "Month 1-3: Python, Statistics, Mathematics",
            "Month 4-6: Machine Learning (Scikit-learn, TensorFlow)",
            "Month 7-9: Data Analysis (Pandas, NumPy, Visualization)",
            "Month 10-12: Deep Learning, NLP, Computer Vision",
            "Year 2: Big Data (Spark, Hadoop), Cloud ML",
            "Year 3: Real-world Projects, Kaggle Competitions"
        ],
        "Business Analyst": [
            "Month 1-3: Excel, SQL, Business Fundamentals",
            "Month 4-6: Data Visualization (Tableau, Power BI)",
            "Month 7-9: Business Intelligence, Analytics",
            "Month 10-12: Project Management, Agile",
            "Year 2: Domain Knowledge, Case Studies",
            "Year 3: Certifications (CBAP, PMI-PBA)"
        ],
        "Digital Marketer": [
            "Month 1-3: SEO, Content Marketing, Social Media",
            "Month 4-6: Google Ads, Facebook Ads, Analytics",
            "Month 7-9: Email Marketing, Marketing Automation",
            "Month 10-12: Build Portfolio, Client Projects",
            "Year 2: Advanced Analytics, Conversion Optimization",
            "Year 3: Strategy, Team Management"
        ],
        "Web Developer": [
            "Month 1-3: HTML, CSS, JavaScript Fundamentals",
            "Month 4-6: React/Vue/Angular, Frontend Frameworks",
            "Month 7-9: Backend (Node.js/Python), Databases",
            "Month 10-12: Full Stack Projects, Deployment",
            "Year 2: Advanced Topics, Testing, CI/CD",
            "Year 3: System Design, Scalability, Architecture"
        ],
        "Game Developer": [
            "Month 1-3: Learn Unity/Unreal Engine, C#/C++ Basics",
            "Month 4-6: 3D Modeling (Blender), Game Physics",
            "Month 7-9: Game Design, Level Design, Animation",
            "Month 10-12: Build 2-3 Complete Games, Publish",
            "Year 2: Advanced Graphics, Multiplayer, VR/AR",
            "Year 3: Portfolio, Game Studio or Indie Development"
        ],
        "UI/UX Designer": [
            "Month 1-3: Design Principles, Figma/Sketch, Wireframing",
            "Month 4-6: User Research, Prototyping, Usability Testing",
            "Month 7-9: Visual Design, Typography, Color Theory",
            "Month 10-12: Build Portfolio, Real Client Projects",
            "Year 2: Advanced UX, Design Systems, Accessibility",
            "Year 3: Leadership, Design Strategy, Mentoring"
        ],
        "Graphic Designer": [
            "Month 1-3: Adobe Photoshop, Illustrator, Design Basics",
            "Month 4-6: Typography, Color Theory, Layout Design",
            "Month 7-9: Branding, Logo Design, Print Design",
            "Month 10-12: Build Portfolio, Freelance Projects",
            "Year 2: Motion Graphics, After Effects, 3D Design",
            "Year 3: Creative Direction, Client Management"
        ],
        "Video Editor": [
            "Month 1-3: Adobe Premiere Pro, Final Cut Pro Basics",
            "Month 4-6: Color Grading, Audio Editing, Transitions",
            "Month 7-9: Motion Graphics, After Effects, VFX",
            "Month 10-12: Build Portfolio, YouTube/Client Work",
            "Year 2: Advanced Editing, Storytelling, Cinematography",
            "Year 3: Production Management, Team Leadership"
        ],
        "Agricultural Specialist": [
            "Month 1-6: Study soil science, crop management, irrigation",
            "Month 7-12: Learn modern farming techniques, organic farming",
            "Year 2: Agricultural technology, precision farming, drones",
            "Year 3: Sustainable agriculture, certifications, field projects"
        ],
        "Healthcare Professional": [
            "Month 1-6: Medical fundamentals, patient care basics",
            "Month 7-12: Clinical skills, healthcare systems",
            "Year 2: Specialization, certifications, practical training",
            "Year 3: Advanced practice, research, professional development"
        ],
        "Mechanical Engineer": [
            "Month 1-6: CAD software (AutoCAD, SolidWorks), mechanics",
            "Month 7-12: Thermodynamics, manufacturing processes",
            "Year 2: Design projects, simulations, internships",
            "Year 3: Advanced topics, certifications, industry projects"
        ],
        "Civil Engineer": [
            "Month 1-6: Structural analysis, construction materials",
            "Month 7-12: CAD, surveying, project management",
            "Year 2: Design software, site visits, practical training",
            "Year 3: Certifications, major projects, professional practice"
        ],
        "Electrical Engineer": [
            "Month 1-6: Circuit design, electronics fundamentals",
            "Month 7-12: Power systems, control systems, PCB design",
            "Year 2: Embedded systems, automation, lab projects",
            "Year 3: Advanced topics, certifications, industry experience"
        ],
        "Engineer": [
            "Month 1-6: Engineering fundamentals, technical drawing",
            "Month 7-12: Specialized knowledge in your field",
            "Year 2: Practical projects, internships, certifications",
            "Year 3: Advanced skills, professional development, networking"
        ],
        # Add more careers and their roadmaps here...
"Cyber Security Analyst": [
"Month 1-3: Networking Basics, Linux Fundamentals, Security Basics",
"Month 4-6: Ethical Hacking, Penetration Testing Tools",
"Month 7-9: Security Monitoring, SIEM Tools",
"Month 10-12: Build Security Labs, Vulnerability Assessments",
"Year 2: Advanced Security (Cloud Security, Malware Analysis)",
"Year 3: Certifications (CEH, CISSP), Security Research"
],

"Cloud Engineer": [
"Month 1-3: Linux, Networking, Virtualization Basics",
"Month 4-6: Learn AWS/Azure/GCP Core Services",
"Month 7-9: Cloud Deployment, Containers (Docker)",
"Month 10-12: Build Cloud Projects, CI/CD Pipelines",
"Year 2: Kubernetes, Infrastructure as Code (Terraform)",
"Year 3: Cloud Architecture, Advanced Certifications"
],

"DevOps Engineer": [
"Month 1-3: Linux, Git, Networking Fundamentals",
"Month 4-6: CI/CD Tools (Jenkins, GitHub Actions)",
"Month 7-9: Docker, Kubernetes, Infrastructure Automation",
"Month 10-12: Build CI/CD Pipelines and Deployment Projects",
"Year 2: Monitoring Tools (Prometheus, Grafana)",
"Year 3: DevOps Architecture and Scaling"
],

"AI Engineer": [
"Month 1-3: Python, Linear Algebra, Statistics",
"Month 4-6: Machine Learning Algorithms",
"Month 7-9: Deep Learning (TensorFlow, PyTorch)",
"Month 10-12: AI Projects (Chatbots, Recommendation Systems)",
"Year 2: NLP, Computer Vision",
"Year 3: AI Research, Production AI Systems"
],

"Machine Learning Engineer": [
"Month 1-3: Python, Statistics, Linear Algebra",
"Month 4-6: ML Algorithms and Scikit-learn",
"Month 7-9: Deep Learning Frameworks",
"Month 10-12: Build ML Models and Deploy",
"Year 2: MLOps and Model Optimization",
"Year 3: Advanced ML Systems"
],

"Database Administrator": [
"Month 1-3: SQL Fundamentals, Database Concepts",
"Month 4-6: MySQL, PostgreSQL Administration",
"Month 7-9: Backup, Recovery, Security",
"Month 10-12: Database Optimization and Indexing",
"Year 2: Distributed Databases",
"Year 3: Database Architecture"
],

"Network Engineer": [
"Month 1-3: Networking Fundamentals (TCP/IP)",
"Month 4-6: Routing and Switching",
"Month 7-9: Network Security and Firewalls",
"Month 10-12: Build Network Labs",
"Year 2: Advanced Networking (SDN)",
"Year 3: Certifications (CCNA, CCNP)"
],

"Blockchain Developer": [
"Month 1-3: Programming Basics (JavaScript, Solidity)",
"Month 4-6: Blockchain Fundamentals",
"Month 7-9: Smart Contract Development",
"Month 10-12: Build DApps",
"Year 2: Advanced Blockchain Architecture",
"Year 3: Web3 and DeFi Projects"
],

"AR/VR Developer": [
"Month 1-3: Unity/Unreal Basics",
"Month 4-6: 3D Modeling and Interaction Design",
"Month 7-9: AR/VR SDKs",
"Month 10-12: Build VR/AR Applications",
"Year 2: Multiplayer VR and Advanced Graphics",
"Year 3: Industry Projects"
],

"IoT Developer": [
"Month 1-3: Electronics Basics, Microcontrollers",
"Month 4-6: Arduino, Raspberry Pi",
"Month 7-9: IoT Communication Protocols",
"Month 10-12: Build IoT Devices and Apps",
"Year 2: Edge Computing",
"Year 3: Industrial IoT Solutions"
],

"Embedded Systems Engineer": [
"Month 1-3: C Programming, Microcontrollers",
"Month 4-6: Embedded Linux",
"Month 7-9: Device Drivers and RTOS",
"Month 10-12: Embedded Projects",
"Year 2: Hardware Design",
"Year 3: Industrial Embedded Systems"
],

"QA Engineer": [
"Month 1-3: Software Testing Fundamentals",
"Month 4-6: Manual Testing and Test Cases",
"Month 7-9: Automation Testing (Selenium)",
"Month 10-12: CI/CD Testing Integration",
"Year 2: Performance Testing",
"Year 3: Test Architecture"
],

"Automation Engineer": [
"Month 1-3: Programming Basics (Python/Java)",
"Month 4-6: Selenium and Automation Tools",
"Month 7-9: Framework Development",
"Month 10-12: Build Automated Test Suites",
"Year 2: Performance and Security Testing",
"Year 3: Automation Architecture"
],

"Product Manager": [
"Month 1-3: Product Management Basics",
"Month 4-6: Market Research and User Needs",
"Month 7-9: Agile and Scrum",
"Month 10-12: Product Roadmap Planning",
"Year 2: Product Analytics",
"Year 3: Product Leadership"
],

"Project Manager": [
"Month 1-3: Project Management Basics",
"Month 4-6: Agile and Scrum Methodology",
"Month 7-9: Risk Management",
"Month 10-12: Project Planning Tools",
"Year 2: Team Leadership",
"Year 3: Certifications (PMP)"
],

"Technical Writer": [
"Month 1-3: Writing Skills and Documentation Basics",
"Month 4-6: API Documentation",
"Month 7-9: Tools (Markdown, Docs Platforms)",
"Month 10-12: Build Documentation Portfolio",
"Year 2: Advanced Technical Writing",
"Year 3: Documentation Leadership"
],

"SEO Specialist": [
"Month 1-3: SEO Fundamentals",
"Month 4-6: Keyword Research",
"Month 7-9: Technical SEO",
"Month 10-12: Website Optimization Projects",
"Year 2: SEO Analytics",
"Year 3: SEO Strategy"
],

"Content Writer": [
"Month 1-3: Writing Fundamentals",
"Month 4-6: SEO Content Writing",
"Month 7-9: Blogging and Copywriting",
"Month 10-12: Portfolio Building",
"Year 2: Content Strategy",
"Year 3: Content Leadership"
],

"Social Media Manager": [
"Month 1-3: Social Media Platforms Basics",
"Month 4-6: Content Planning",
"Month 7-9: Analytics and Growth",
"Month 10-12: Campaign Management",
"Year 2: Brand Strategy",
"Year 3: Team Leadership"
],

"Product Designer": [
"Month 1-3: Design Principles",
"Month 4-6: UI/UX Tools",
"Month 7-9: Prototyping",
"Month 10-12: Portfolio Projects",
"Year 2: Design Systems",
"Year 3: Product Strategy"
],

"Animator": [
"Month 1-3: Animation Basics",
"Month 4-6: 2D Animation Tools",
"Month 7-9: 3D Animation",
"Month 10-12: Animation Projects",
"Year 2: Advanced Animation",
"Year 3: Film/Game Projects"
],

"Photographer": [
"Month 1-3: Camera Basics",
"Month 4-6: Lighting Techniques",
"Month 7-9: Photo Editing",
"Month 10-12: Portfolio Projects",
"Year 2: Commercial Photography",
"Year 3: Studio Management"
],

"Content Creator": [
"Month 1-3: Platform Basics (YouTube/Instagram)",
"Month 4-6: Video Production",
"Month 7-9: Editing and Branding",
"Month 10-12: Audience Growth",
"Year 2: Monetization",
"Year 3: Brand Partnerships"
],

"Ethical Hacker": [
"Month 1-3: Networking and Linux",
"Month 4-6: Hacking Tools",
"Month 7-9: Penetration Testing",
"Month 10-12: Security Labs",
"Year 2: Red Teaming",
"Year 3: Security Certifications"
],

"Robotics Engineer": [
"Month 1-3: Electronics and Programming",
"Month 4-6: Robotics Frameworks",
"Month 7-9: Sensors and Actuators",
"Month 10-12: Robotics Projects",
"Year 2: AI Robotics",
"Year 3: Industrial Robotics"
],

"Supply Chain Analyst": [
"Month 1-3: Logistics Basics",
"Month 4-6: Data Analysis",
"Month 7-9: Supply Chain Tools",
"Month 10-12: Process Optimization",
"Year 2: Advanced Analytics",
"Year 3: Supply Chain Strategy"
],

"Financial Analyst": [
"Month 1-3: Accounting Basics",
"Month 4-6: Financial Modeling",
"Month 7-9: Data Analysis",
"Month 10-12: Investment Analysis",
"Year 2: Advanced Finance",
"Year 3: Certifications (CFA)"
],

"Economist": [
"Month 1-3: Microeconomics",
"Month 4-6: Macroeconomics",
"Month 7-9: Econometrics",
"Month 10-12: Data Analysis",
"Year 2: Policy Research",
"Year 3: Economic Consulting"
],

"Statistician": [
"Month 1-3: Probability",
"Month 4-6: Statistical Methods",
"Month 7-9: Data Modeling",
"Month 10-12: Statistical Software",
"Year 2: Advanced Statistics",
"Year 3: Research Projects"
],

"Research Scientist": [
"Month 1-3: Research Methodology",
"Month 4-6: Literature Review",
"Month 7-9: Experimental Design",
"Month 10-12: Publish Research",
"Year 2: Advanced Research",
"Year 3: Scientific Leadership"
],

"Site Reliability Engineer": [
"Month 1-3: Linux, Networking, System Administration Basics",
"Month 4-6: Monitoring Tools (Prometheus, Grafana)",
"Month 7-9: Automation with Python/Bash",
"Month 10-12: Build Reliable Infrastructure Projects",
"Year 2: Kubernetes, Distributed Systems",
"Year 3: Reliability Engineering and Scaling"
],

"Solutions Architect": [
"Month 1-3: Software Architecture Fundamentals",
"Month 4-6: Cloud Platforms (AWS/Azure/GCP)",
"Month 7-9: System Design and Integration",
"Month 10-12: Architecture Case Studies",
"Year 2: Enterprise Architecture",
"Year 3: Advanced Cloud Architecture"
],

"IT Support Specialist": [
"Month 1-3: Computer Hardware and OS Basics",
"Month 4-6: Networking and Troubleshooting",
"Month 7-9: System Administration",
"Month 10-12: Help Desk Tools and Ticket Systems",
"Year 2: Advanced IT Infrastructure",
"Year 3: IT Management"
],

"Technical Support Engineer": [
"Month 1-3: Operating Systems and Networking",
"Month 4-6: Troubleshooting and Diagnostics",
"Month 7-9: Customer Support Tools",
"Month 10-12: System Maintenance Projects",
"Year 2: Advanced Technical Support",
"Year 3: Support Team Leadership"
],

"Systems Administrator": [
"Month 1-3: Linux/Windows Server Basics",
"Month 4-6: Network Configuration",
"Month 7-9: Security and Backup Systems",
"Month 10-12: Server Deployment Projects",
"Year 2: Virtualization and Cloud",
"Year 3: Infrastructure Architecture"
],

"Data Engineer": [
"Month 1-3: Python, SQL, Data Processing Basics",
"Month 4-6: ETL Pipelines and Data Warehousing",
"Month 7-9: Big Data Tools (Spark, Hadoop)",
"Month 10-12: Data Pipeline Projects",
"Year 2: Cloud Data Platforms",
"Year 3: Data Architecture"
],

"Prompt Engineer": [
"Month 1-3: Basics of AI and NLP",
"Month 4-6: Prompt Design and Optimization",
"Month 7-9: LLM APIs and AI Tools",
"Month 10-12: AI Application Projects",
"Year 2: Advanced Prompt Engineering",
"Year 3: AI Product Development"
],

"Bioinformatics Specialist": [
"Month 1-3: Biology and Programming Basics",
"Month 4-6: Genomics and Data Analysis",
"Month 7-9: Bioinformatics Tools",
"Month 10-12: Research Projects",
"Year 2: Advanced Bioinformatics",
"Year 3: Genomic Data Research"
],

"Digital Product Designer": [
"Month 1-3: Design Principles and Tools",
"Month 4-6: UX Research and Wireframing",
"Month 7-9: Prototyping and User Testing",
"Month 10-12: Portfolio Projects",
"Year 2: Design Systems",
"Year 3: Product Strategy"
],

"E-commerce Manager": [
"Month 1-3: E-commerce Platforms Basics",
"Month 4-6: Product Listings and SEO",
"Month 7-9: Digital Marketing for E-commerce",
"Month 10-12: Store Optimization Projects",
"Year 2: Sales Analytics",
"Year 3: E-commerce Strategy"
],

"Logistics Manager": [
"Month 1-3: Supply Chain Basics",
"Month 4-6: Inventory Management",
"Month 7-9: Logistics Software Tools",
"Month 10-12: Distribution Projects",
"Year 2: Global Logistics",
"Year 3: Logistics Strategy"
],

"Operations Manager": [
"Month 1-3: Business Operations Basics",
"Month 4-6: Process Optimization",
"Month 7-9: Operations Analytics",
"Month 10-12: Process Improvement Projects",
"Year 2: Leadership Skills",
"Year 3: Operations Strategy"
],

"Marketing Analyst": [
"Month 1-3: Marketing Fundamentals",
"Month 4-6: Data Analysis Tools",
"Month 7-9: Marketing Analytics",
"Month 10-12: Campaign Analysis Projects",
"Year 2: Advanced Analytics",
"Year 3: Marketing Strategy"
],

"HR Specialist": [
"Month 1-3: HR Fundamentals",
"Month 4-6: Recruitment and Talent Management",
"Month 7-9: HR Tools and Analytics",
"Month 10-12: HR Policy Development",
"Year 2: Organizational Development",
"Year 3: HR Leadership"
],

"Instructional Designer": [
"Month 1-3: Learning Theory Basics",
"Month 4-6: Instructional Design Models",
"Month 7-9: E-learning Tools",
"Month 10-12: Course Development Projects",
"Year 2: Learning Analytics",
"Year 3: Educational Strategy"
],

"3D Artist": [
"Month 1-3: 3D Modeling Basics",
"Month 4-6: Texturing and Lighting",
"Month 7-9: Animation Tools",
"Month 10-12: Portfolio Projects",
"Year 2: Advanced 3D Graphics",
"Year 3: Industry Projects"
],

"Sound Engineer": [
"Month 1-3: Audio Recording Basics",
"Month 4-6: Audio Editing Tools",
"Month 7-9: Sound Design",
"Month 10-12: Audio Production Projects",
"Year 2: Advanced Sound Engineering",
"Year 3: Studio Production"
],

"Film Director": [
"Month 1-3: Film Theory and Storytelling",
"Month 4-6: Cinematography Basics",
"Month 7-9: Film Editing",
"Month 10-12: Short Film Projects",
"Year 2: Advanced Filmmaking",
"Year 3: Feature Film Production"
],

"Journalist": [
"Month 1-3: Journalism Basics",
"Month 4-6: News Writing",
"Month 7-9: Investigative Reporting",
"Month 10-12: Portfolio Development",
"Year 2: Media Ethics",
"Year 3: Senior Journalism Roles"
],

"Public Relations Specialist": [
"Month 1-3: PR Fundamentals",
"Month 4-6: Media Communication",
"Month 7-9: Campaign Planning",
"Month 10-12: PR Projects",
"Year 2: Brand Management",
"Year 3: PR Strategy"
],

"Lawyer": [
"Month 1-6: Study legal fundamentals, constitution, and legal writing",
"Month 7-12: Case law analysis, internships in law firms",
"Year 2: Specialize in corporate, criminal, or civil law",
"Year 3: Practice in courts, build professional network"
],

"Chartered Accountant": [
"Month 1-6: Accounting principles, taxation basics",
"Month 7-12: Financial reporting and auditing",
"Year 2: Advanced taxation and financial management",
"Year 3: Certification exams and professional practice"
],

"Teacher": [
"Month 1-6: Teaching methodologies and subject knowledge",
"Month 7-12: Classroom management and lesson planning",
"Year 2: Practical teaching experience and certifications",
"Year 3: Educational leadership and curriculum development"
],

"Professor": [
"Month 1-6: Advanced subject research and academic writing",
"Month 7-12: Teaching assistantship and lectures",
"Year 2: Publish research papers and attend conferences",
"Year 3: Academic specialization and university teaching"
],

"Psychologist": [
"Month 1-6: Psychology fundamentals and human behavior",
"Month 7-12: Counseling techniques and case studies",
"Year 2: Clinical psychology training",
"Year 3: Professional practice and research"
],

"Architect": [
"Month 1-6: Architectural design basics, drawing, CAD",
"Month 7-12: Building materials and structural design",
"Year 2: Design projects and internships",
"Year 3: Professional architecture practice"
],

"Interior Designer": [
"Month 1-6: Design fundamentals and color theory",
"Month 7-12: CAD and 3D design tools",
"Year 2: Interior design projects and client work",
"Year 3: Portfolio and professional design practice"
],

"Fashion Designer": [
"Month 1-6: Fashion design basics and sketching",
"Month 7-12: Textile knowledge and garment construction",
"Year 2: Fashion collections and portfolio",
"Year 3: Fashion industry internships or brand launch"
],

"Chef": [
"Month 1-6: Culinary basics and kitchen management",
"Month 7-12: International cuisines and food presentation",
"Year 2: Restaurant internships",
"Year 3: Professional chef specialization"
],

"Hotel Manager": [
"Month 1-6: Hospitality management basics",
"Month 7-12: Customer service and hotel operations",
"Year 2: Internship in hotels or resorts",
"Year 3: Hotel management leadership roles"
],

"Tourism Manager": [
"Month 1-6: Tourism industry basics",
"Month 7-12: Travel planning and destination management",
"Year 2: Tourism marketing and internships",
"Year 3: Tourism business management"
],

"Event Manager": [
"Month 1-6: Event planning fundamentals",
"Month 7-12: Vendor coordination and budgeting",
"Year 2: Event marketing and logistics",
"Year 3: Managing large scale events"
],

"Real Estate Agent": [
"Month 1-6: Real estate market fundamentals",
"Month 7-12: Property management and negotiation",
"Year 2: Real estate sales and marketing",
"Year 3: Real estate investment strategies"
],

"Entrepreneur": [
"Month 1-6: Business fundamentals and startup ideas",
"Month 7-12: Market research and business planning",
"Year 2: Launch startup and manage operations",
"Year 3: Business scaling and investment"
],

"Startup Founder": [
"Month 1-6: Startup ecosystem and product ideas",
"Month 7-12: MVP development and customer validation",
"Year 2: Funding and growth strategies",
"Year 3: Business expansion"
],

"Sales Manager": [
"Month 1-6: Sales techniques and communication skills",
"Month 7-12: Customer relationship management",
"Year 2: Sales analytics and strategy",
"Year 3: Sales team leadership"
],

"Retail Manager": [
"Month 1-6: Retail operations and merchandising",
"Month 7-12: Customer experience management",
"Year 2: Retail analytics and supply chain",
"Year 3: Retail store management"
],

"Pilot": [
"Month 1-6: Aviation fundamentals and flight theory",
"Month 7-12: Flight simulator training",
"Year 2: Pilot license training",
"Year 3: Commercial flight experience"
],

"Air Traffic Controller": [
"Month 1-6: Aviation communication and regulations",
"Month 7-12: Radar systems and navigation",
"Year 2: Air traffic control training",
"Year 3: Advanced traffic management"
],

"Police Officer": [
"Month 1-6: Law enforcement basics",
"Month 7-12: Physical and tactical training",
"Year 2: Field operations training",
"Year 3: Specialized policing units"
],

"Firefighter": [
"Month 1-6: Fire safety and emergency response",
"Month 7-12: Rescue training and equipment use",
"Year 2: Fire department field training",
"Year 3: Advanced rescue operations"
],

"Social Worker": [
"Month 1-6: Social work fundamentals",
"Month 7-12: Community service and counseling",
"Year 2: NGO or social organization internships",
"Year 3: Social policy and leadership"
],

"Political Analyst": [
"Month 1-6: Political science fundamentals",
"Month 7-12: Policy analysis and research",
"Year 2: Government internships",
"Year 3: Political consulting"
],

"Diplomat": [
"Month 1-6: International relations basics",
"Month 7-12: Diplomacy and foreign policy",
"Year 2: Government training programs",
"Year 3: International diplomatic assignments"
],

"Historian": [
"Month 1-6: Historical research methods",
"Month 7-12: Archival research",
"Year 2: Historical writing and publications",
"Year 3: Academic or museum career"
]

    }
    
    # Return specific roadmap or create generic one
    if career in roadmaps:
        return roadmaps[career]
    else:
        # Generic roadmap for any field
        return [
            f"Month 1-6: Build foundational skills in {career}",
            f"Month 7-12: Gain practical experience through projects",
            f"Year 2: Specialize and get relevant certifications",
            f"Year 3: Build professional network and portfolio in {career}"
        ]

# -------------------------------------------------
# Multi-Model Ensemble Prediction
# -------------------------------------------------
def ensemble_prediction(study_hours, attendance, previous_marks, programming_skill, communication_skill):
    try:
        perf_input = np.array([[study_hours, attendance, previous_marks,
                                programming_skill, communication_skill]])
        
        # Load or create multiple models
        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeRegressor
        
        # Use existing model
        rf_pred = performance_model.predict(perf_input)[0]
        
        # Create and train additional models on-the-fly
        df = pd.read_csv("student_data.csv")
        X = df[["StudyHours", "Attendance", "PreviousMarks", "ProgrammingSkill", "CommunicationSkill"]]
        y = df["Marks"]
        
        lr_model = LinearRegression()
        lr_model.fit(X, y)
        lr_pred = lr_model.predict(perf_input)[0]
        
        dt_model = DecisionTreeRegressor(random_state=42)
        dt_model.fit(X, y)
        dt_pred = dt_model.predict(perf_input)[0]
        
        # Ensemble: Average of all models
        ensemble_pred = (rf_pred + lr_pred + dt_pred) / 3
        
        return {
            "ensemble": round(float(ensemble_pred), 2),
            "randomForest": round(float(rf_pred), 2),
            "linearRegression": round(float(lr_pred), 2),
            "decisionTree": round(float(dt_pred), 2)
        }
    except:
        return None


# -------------------------------------------------
# Interest Mapping Function (GLOBAL - ALL FIELDS)
# -------------------------------------------------
def map_interest(user_interest):

    user_interest = user_interest.lower()

    # IT/Software Development
    it_keywords = [
        "web", "software", "coding", "programming", "developer", "development",
        "android", "ios", "mobile", "app", "application",
        "java", "python", "javascript", "react", "node", "angular",
        "backend", "frontend", "fullstack", "full stack",
        "cyber", "security", "hacking", "ethical",
        "ai", "ml", "machine learning", "artificial intelligence",
        "data science", "data", "analytics", "big data",
        "cloud", "aws", "azure", "devops", "docker", "kubernetes",
        "database", "sql", "mongodb", "api", "rest"
    ]
    
    # Creative/Design
    creative_keywords = [
        "design", "designer", "graphic", "ui", "ux", "user interface",
        "art", "artist", "creative", "illustration", "illustrator",
        "animation", "animator", "video", "editing", "photoshop",
        "figma", "sketch", "adobe", "visual", "branding",
        "game", "3d", "unity", "unreal", "blender"
    ]
    
    # Management/Business
    management_keywords = [
        "business", "management", "manager", "mba", "admin",
        "marketing", "digital marketing", "seo", "social media",
        "finance", "accounting", "sales", "hr", "human resource",
        "project management", "product management", "consulting",
        "entrepreneur", "startup", "strategy"
    ]
    
    # Research/Academic
    research_keywords = [
        "research", "researcher", "scientist", "science",
        "analysis", "analyst", "lab", "laboratory",
        "phd", "academic", "professor", "teaching",
        "biology", "chemistry", "physics", "mathematics"
    ]
    
    # Agriculture
    agriculture_keywords = [
        "agriculture", "farming", "crop", "soil", "agri",
        "horticulture", "agronomy", "agricultural", "farm"
    ]
    
    # Medical/Healthcare
    medical_keywords = [
        "medical", "medicine", "doctor", "healthcare", "health",
        "nursing", "pharmacy", "hospital", "clinical"
    ]
    
    # Engineering (Non-IT)
    engineering_keywords = [
        "mechanical", "civil", "electrical", "electronics",
        "automobile", "chemical", "aerospace"
    ]

    # Check for matches
    if any(word in user_interest for word in it_keywords):
        return "IT"
    elif any(word in user_interest for word in creative_keywords):
        return "Creative"
    elif any(word in user_interest for word in management_keywords):
        return "Management"
    elif any(word in user_interest for word in research_keywords):
        return "Research"
    elif any(word in user_interest for word in agriculture_keywords):
        return "Agriculture"
    elif any(word in user_interest for word in medical_keywords):
        return "Medical"
    elif any(word in user_interest for word in engineering_keywords):
        return "Engineering"
    else:
        return "General"


# -------------------------------------------------
# Prediction API
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.json

        # Validation
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ["studyHours", "attendance", "previousMarks", 
                          "programmingSkill", "communicationSkill", "interestArea"]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        study_hours = float(data["studyHours"])
        attendance = float(data["attendance"])
        previous_marks = float(data["previousMarks"])
        programming_skill = int(data["programmingSkill"])
        communication_skill = int(data["communicationSkill"])
        user_interest = str(data["interestArea"]).strip()

        # Range validation
        if not (0 <= study_hours <= 24):
            return jsonify({"error": "Study hours must be between 0-24"}), 400
        if not (0 <= attendance <= 100):
            return jsonify({"error": "Attendance must be between 0-100"}), 400
        if not (0 <= previous_marks <= 100):
            return jsonify({"error": "Previous marks must be between 0-100"}), 400
        if programming_skill not in [0, 1, 2, 3]:
            return jsonify({"error": "Programming skill must be 0, 1, 2, or 3"}), 400
        if communication_skill not in [1, 2, 3]:
            return jsonify({"error": "Communication skill must be 1, 2, or 3"}), 400
        if not user_interest:
            return jsonify({"error": "Interest area cannot be empty"}), 400

        # Map user interest
        mapped_interest = map_interest(user_interest)

        # Encode mapped interest - handle unknown categories
        try:
            interest_encoded = interest_encoder.transform([mapped_interest])[0]
        except ValueError:
            # If mapped_interest not in encoder, use a default (IT)
            interest_encoded = interest_encoder.transform(["IT"])[0]

        # Performance Prediction
        perf_input = np.array([[study_hours, attendance, previous_marks,
                                programming_skill, communication_skill]])

        predicted_marks = performance_model.predict(perf_input)[0]
        predicted_marks = max(0, min(100, predicted_marks))  # Clamp between 0-100

        # Career Prediction with Rule-Based Override
        career_input = np.array([[predicted_marks,
                                  programming_skill,
                                  communication_skill,
                                  interest_encoded]])

        predicted_career_encoded = career_model.predict(career_input)[0]
        predicted_career = career_encoder.inverse_transform([predicted_career_encoded])[0]
        
        # RULE-BASED CAREER PREDICTION (GLOBAL)
        user_interest_lower = user_interest.lower()
        
        if mapped_interest == "IT":
            # IT Careers based on specific interest
            if "android" in user_interest_lower or "mobile" in user_interest_lower or "app" in user_interest_lower:
                predicted_career = "Android Developer"
            elif "web" in user_interest_lower or "frontend" in user_interest_lower:
                predicted_career = "Web Developer"
            elif "data" in user_interest_lower or "ml" in user_interest_lower or "ai" in user_interest_lower:
                predicted_career = "Data Scientist"
            else:
                predicted_career = "Software Engineer"
        
        elif mapped_interest == "Creative":
            # Creative Careers
            if "game" in user_interest_lower or "3d" in user_interest_lower or "unity" in user_interest_lower:
                predicted_career = "Game Developer"
            elif "ui" in user_interest_lower or "ux" in user_interest_lower:
                predicted_career = "UI/UX Designer"
            elif "graphic" in user_interest_lower or "photoshop" in user_interest_lower:
                predicted_career = "Graphic Designer"
            elif "video" in user_interest_lower or "animation" in user_interest_lower:
                predicted_career = "Video Editor"
            else:
                predicted_career = "Graphic Designer"
        
        elif mapped_interest == "Management":
            predicted_career = "Business Analyst"
        
        elif mapped_interest == "Research":
            predicted_career = "Data Scientist"
        
        elif mapped_interest == "Agriculture":
            predicted_career = "Agricultural Specialist"
        
        elif mapped_interest == "Medical":
            predicted_career = "Healthcare Professional"
        
        elif mapped_interest == "Engineering":
            if "mechanical" in user_interest_lower:
                predicted_career = "Mechanical Engineer"
            elif "civil" in user_interest_lower:
                predicted_career = "Civil Engineer"
            elif "electrical" in user_interest_lower or "electronics" in user_interest_lower:
                predicted_career = "Electrical Engineer"
            else:
                predicted_career = "Engineer"
        
        else:
            # General career based on user interest
            predicted_career = user_interest.title() + " Specialist"
        
        # Career confidence
        if hasattr(career_model, 'predict_proba'):
            career_proba = career_model.predict_proba(career_input)[0]
            career_confidence = round(float(max(career_proba)) * 100, 2)
        else:
            career_confidence = 85.0
        
        # Performance category
        performance_category = get_performance_category(predicted_marks)
        
        # Weak areas detection
        weak_areas = detect_weak_areas(study_hours, attendance, previous_marks, 
                                       programming_skill, communication_skill)
        
        # Recommendations
        recommendations = get_recommendations(weak_areas, predicted_marks)
        
        # Career Roadmap
        career_roadmap = generate_career_roadmap(predicted_career)
        
        # Ensemble Prediction
        ensemble_results = ensemble_prediction(study_hours, attendance, previous_marks,
                                              programming_skill, communication_skill)

        return jsonify({
            "predictedMarks": round(float(predicted_marks), 2),
            "predictedCareer": predicted_career,
            "mappedInterest": mapped_interest,
            "performanceCategory": performance_category,
            "careerConfidence": career_confidence,
            "weakAreas": weak_areas,
            "recommendations": recommendations,
            "careerRoadmap": career_roadmap,
            "ensemblePrediction": ensemble_results
        })

    except ValueError as e:
        return jsonify({"error": f"Invalid data type: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


# -------------------------------------------------
# Model Comparison API
# -------------------------------------------------
@app.route("/model-comparison", methods=["GET"])
def model_comparison():
    try:
        df = pd.read_csv("student_data.csv")
        
        X_perf = df[["StudyHours", "Attendance", "PreviousMarks", "ProgrammingSkill", "CommunicationSkill"]]
        y_perf = df["Marks"]
        
        # Test different models
        from sklearn.linear_model import LinearRegression
        
        lr_model = LinearRegression()
        lr_model.fit(X_perf, y_perf)
        lr_pred = lr_model.predict(X_perf)
        lr_mse = mean_squared_error(y_perf, lr_pred)
        
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_perf, y_perf)
        rf_pred = rf_model.predict(X_perf)
        rf_mse = mean_squared_error(y_perf, rf_pred)
        
        comparison = {
            "Linear Regression": {
                "MSE": round(lr_mse, 2),
                "Accuracy": round(100 - lr_mse, 2)
            },
            "Random Forest": {
                "MSE": round(rf_mse, 2),
                "Accuracy": round(100 - rf_mse, 2)
            }
        }
        
        return jsonify(comparison)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host="0.0.0.0", port=port)
