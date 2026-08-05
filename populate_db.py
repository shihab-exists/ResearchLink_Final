# Database Seeding Script for ResearchLink
# This script populates the MySQL database with 20+ realistic records per table
# Run: python populate_db.py

import os
import django
import random

# Initialize Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'researchlink.settings')
django.setup()

from django.contrib.auth.models import User
from teachers.models import Department, ResearchField, Teacher
from students.models import Skill, Student
from projects.models import Project, Application
from messaging.models import Message

def seed_database():
    print("Starting database seeding...")

    # Clear existing data in our custom tables (respecting foreign key order)
    print("Clearing old records...")
    Message.objects.all().delete()
    Application.objects.all().delete()
    Project.objects.all().delete()
    
    # Delete custom profiles and junction mappings
    Student.objects.all().delete()
    Teacher.objects.all().delete()
    
    # Clear metadata
    Department.objects.all().delete()
    ResearchField.objects.all().delete()
    Skill.objects.all().delete()

    # Clear auth users except system superusers if any
    User.objects.filter(is_superuser=False).delete()
    
    # Ensure admin exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@researchlink.edu', 'admin123')
        print("Admin superuser created: admin / admin123")

    # 1. Populate Departments (21 departments)
    dept_data = [
        ("Computer Science & Engineering", "CSE"),
        ("Electrical & Electronic Engineering", "EEE"),
        ("Mechanical Engineering", "ME"),
        ("Civil Engineering", "CE"),
        ("Industrial & Production Engineering", "IPE"),
        ("Software Engineering", "SWE"),
        ("Information Technology", "IT"),
        ("Biomedical Engineering", "BME"),
        ("Textile Engineering", "TE"),
        ("Chemical Engineering", "ChE"),
        ("Pharmacy", "PHR"),
        ("Mathematics", "MAT"),
        ("Physics", "PHY"),
        ("Chemistry", "CHM"),
        ("Architecture", "ARC"),
        ("Business Administration", "BBA"),
        ("Economics", "ECO"),
        ("English", "ENG"),
        ("Environmental Science", "EVS"),
        ("Law & Justice", "LAW"),
        ("Statistics", "STA")
    ]
    departments = []
    for name, code in dept_data:
        dept = Department.objects.create(name=name, code=code)
        departments.append(dept)
    print(f"Created {len(departments)} departments.")

    # 2. Populate Research Fields (21 fields)
    fields_data = [
        "Artificial Intelligence", "Natural Language Processing", "Machine Learning", 
        "Computer Vision", "Cyber Security", "Blockchain Technology", 
        "Cloud Computing", "Internet of Things (IoT)", "Bioinformatics", 
        "Data Science & Analytics", "Quantum Computing", "Software Engineering", 
        "Robotics & Control", "Nanotechnology", "Renewable Energy", 
        "VLSI & Embedded Systems", "Digital Signal Processing", "Smart Grid Systems", 
        "Wireless Communication", "Material Science", "Human-Computer Interaction"
    ]
    fields = []
    for name in fields_data:
        field = ResearchField.objects.create(name=name)
        fields.append(field)
    print(f"Created {len(fields)} research fields.")

    # 3. Populate Skills (21 skills)
    skills_data = [
        "Python", "SQL", "C++", "Java", "PyTorch", "TensorFlow", "Git & GitHub", 
        "R Programming", "MATLAB", "HTML5 & CSS3", "Vanilla JavaScript", 
        "Linux/Bash", "AWS Cloud", "Docker Containers", "Node.js", 
        "Spring Boot", "Unity 3D Engine", "LaTeX Document Prep", "AutoCAD Design", 
        "Tableau Data Viz", "Microsoft Excel Advanced"
    ]
    skills = []
    for name in skills_data:
        skill = Skill.objects.create(name=name)
        skills.append(skill)
    print(f"Created {len(skills)} skills.")

    # 4. Populate Users & Teachers (20 teachers)
    teacher_first_names = [
        "Anisur", "Lutfur", "Mina", "Tasnim", "Sajid", "Farhana", "Mahbub", 
        "Sultana", "Zaved", "Imran", "Arif", "Nasrin", "Kamal", "Rashed", 
        "Tania", "Shafiq", "Nadia", "Tareq", "Sabrina", "Ziaur"
    ]
    teacher_last_names = [
        "Rahman", "Rahman", "Chowdhury", "Islam", "Hasan", "Ahmed", "Alom", 
        "Begum", "Bari", "Hossain", "Chowdhury", "Jahan", "Uddin", "Karim", 
        "Sultana", "Ahmed", "Yasmin", "Khan", "Alam", "Rashid"
    ]
    designations = ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"]
    teachers = []
    
    for i in range(20):
        username = f"teacher{i+1}"
        email = f"t{i+1}@researchlink.edu"
        first_name = teacher_first_names[i]
        last_name = teacher_last_names[i]
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password="teacher123",
            first_name=first_name,
            last_name=last_name
        )
        
        # Select department and designation
        dept = departments[i % len(departments)]
        designation = designations[i % len(designations)]
        room_no = f"Room {300 + i * 5}"
        bio = f"Experienced academic in {dept.code}. My current research focuses on practical engineering solutions and publications in international journals."
        
        # Approve all except the last 3 (so admin can approve them in dashboard!)
        is_approved = True if i < 17 else False
        
        teacher_profile = Teacher.objects.create(
            user=user,
            dept=dept,
            designation=designation,
            room_no=room_no,
            is_approved=is_approved,
            bio=bio
        )
        
        # Associate 2 to 3 random research interests (M2M)
        assigned_fields = random.sample(fields, random.randint(2, 3))
        teacher_profile.interests.add(*assigned_fields)
        
        teachers.append(teacher_profile)
    print(f"Created {len(teachers)} teacher profiles.")

    # 5. Populate Users & Students (20 students)
    student_first_names = [
        "Sadia", "Rifat", "Adnan", "Tanvir", "Nusrat", "Asif", "Sumaiya", 
        "Fahim", "Farhan", "Ishrat", "Siam", "Afrin", "Abrar", "Mehedi", 
        "Taskin", "Zahin", "Tasmia", "Shakil", "Mahim", "Rafi"
    ]
    student_last_names = [
        "Islam", "Hasan", "Sarker", "Rahman", "Jahan", "Iqbal", "Sharmin", 
        "Chowdhury", "Ahmed", "Ara", "Hossain", "Akter", "Khan", "Hasan", 
        "Rahman", "Ahmed", "Tabassum", "Ahmed", "Siddique", "Chowdhury"
    ]
    
    students = []
    for i in range(20):
        username = f"student{i+1}"
        email = f"s{i+1}@g.researchlink.edu"
        first_name = student_first_names[i]
        last_name = student_last_names[i]
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password="student123",
            first_name=first_name,
            last_name=last_name
        )
        
        dept = departments[i % 5] # Cluster students around the first 5 departments (CSE, EEE, ME, CE, IPE) for realistic densities
        roll_no = f"2023-1-60-{100 + (i+1):03d}"
        cgpa = round(random.uniform(2.80, 3.98), 2)
        bio = f"Passionate student looking for research collaboration in CSE and related sectors. Seeking supervision for thesis work."
        cv_url = f"/media/cvs/cv_{username}.pdf"
        
        student_profile = Student.objects.create(
            user=user,
            dept=dept,
            roll_no=roll_no,
            cgpa=cgpa,
            bio=bio,
            cv_url=cv_url
        )
        
        # Associate 3 to 4 random skills (M2M)
        assigned_skills = random.sample(skills, random.randint(3, 4))
        student_profile.skills.add(*assigned_skills)
        
        students.append(student_profile)
    print(f"Created {len(students)} student profiles.")

    # 6. Populate Projects / Opportunities (20 projects)
    project_topics = [
        ("Automated Traffic Management using Computer Vision", "Developing a real-time smart traffic signal controller using YOLO and deep learning algorithms.", "Strong background in Python, PyTorch, and OpenCV is required."),
        ("Securing Electronic Medical Records with Blockchain", "Implementing a decentralized permissioned Hyperledger network for secure storage of health records.", "Familiarity with Docker, cryptography, and Go/Node.js is highly valued."),
        ("Sentiment Analysis of Bengali Local Dialects", "Using Transformers and BERT-based fine-tuning to perform emotion detection on regional Bangla texts.", "Knowledge of NLP, huggingface transformers, and deep learning framework."),
        ("Microgrid Voltage Stability via Intelligent Control", "Designing a PID-tuned stabilizer for distributed grid units incorporating solar arrays.", "Strong background in control systems, MATLAB, and microgrid simulation."),
        ("Design and Prototyping of a Low-cost Solar Tracker", "Building a dual-axis dynamic tracking model to maximize light absorption on rural panels.", "Proficiency in AutoCAD, microcontroller programming (Arduino), and physical mechanics."),
        ("IoT-Based Smart Home Health Monitoring System", "Creating non-invasive sensors integrated with ESP32 to monitor vitals and alert emergency services.", "Experience with IoT hardware development, C++, and basic hardware prototyping."),
        ("Optimization of Supply Chain in Textile Industries", "Developing a linear programming model to minimize shipping delays and raw material costs.", "Background in operations research, linear optimization, and Python."),
        ("Machine Learning for Early Diagnosis of Diabetic Retinopathy", "Classifying fundus photos using residual convolutional neural networks for early clinical risk flags.", "Deep learning expertise, PyTorch, image processing, and datasets processing."),
        ("Smart Agriculture Monitoring with Wireless Sensor Networks", "A LoRaWAN sensor mesh network designed to live-track soil pH, NPK levels, and moisture content.", "Knowledge of wireless communication networks, sensor interfacing, and LoRa protocols."),
        ("Autonomous Robot Navigation in GPS-denied Environments", "Applying SLAM algorithms to a differential drive mobile robot using LIDAR and IMU sensors.", "Experience with ROS (Robot Operating System), C++, and autonomous navigation SLAM."),
        ("Quantum Cryptography: Simulating Post-Quantum Protocols", "Testing lattice-based cryptographic algorithms for resilience against modern attack paradigms.", "Math maturity, knowledge of asymmetric key algorithms, and Python simulations."),
        ("Thermal Comfort and Ventilation Optimization in Eco-Buildings", "Analyzing CFD models to enhance passive cooling structures in sub-tropical institutional blocks.", "Competence in CFD analysis tools (Ansys Fluent) and green building standards."),
        ("Speech Recognition System for Dysarthric Bangla Speakers", "Building acoustic models to improve transcription accuracy for speech-impaired local dialects.", "NLP techniques, speech processing toolkits, and machine learning structures."),
        ("Blockchain-Enabled Academic Credential Verification", "Creating a system to secure, issue, and verify academic certificates using smart contracts.", "Solid understanding of Ethereum, Solidity, and web integration."),
        ("Load Balancing in Multi-Cloud Environments", "An architectural investigation on dynamic round-robin and heuristic load distribution in hybrid clouds.", "Understanding of cloud computing architectures, AWS, and distribution algorithms."),
        ("VLSI Chip Design for Low-Power Wearable Trackers", "A CMOS circuit design optimized for nano-watt power budgets in pacemaker monitoring circuits.", "Background in microelectronic circuits, Cadence virtuoso, and low power layouts."),
        ("Renewable Energy Storage Optimization in Smart Cities", "Using genetic algorithms to find the sweet spot for battery chemistry arrays in urban municipal grids.", "Proficiency in optimization algorithms, MATLAB/Python, and energy storage systems."),
        ("Cybersecurity Vulnerability Assessment of SCADA Networks", "A red-teaming research simulation of threat vectors in critical power infrastructure controllers.", "Familiarity with network security protocols, penetration testing tools, and industrial SCADA."),
        ("Development of an AI-powered Code Review Companion", "A static-analysis tool fine-tuned on custom AST outputs to guide university coding labs.", "Strong understanding of compiler design, abstract syntax trees, and Python."),
        ("Nanomaterial Catalysts for Industrial Wastewater Purification", "synthesizing and testing composite oxides to speed up photocatalytic breakdown of toxic dye streams.", "Background in material synthesis, laboratory spectroscopy, and data analysis.")
    ]
    
    projects = []
    # Approved teachers only can post projects
    approved_teachers = [t for t in teachers if t.is_approved]
    
    for i in range(20):
        title, desc, reqs = project_topics[i]
        teacher = approved_teachers[i % len(approved_teachers)]
        status = "Open" if i < 18 else "Closed"
        
        project = Project.objects.create(
            title=title,
            description=desc,
            requirements=reqs,
            teacher=teacher,
            status=status
        )
        projects.append(project)
    print(f"Created {len(projects)} research projects.")

    # 7. Populate Applications / Requests (20 applications)
    application_messages = [
        "Sir, I am very interested in your smart traffic project. I have strong Python and computer vision skills.",
        "Ma'am, the blockchain verification project perfectly aligns with my thesis interest. Can we collaborate?",
        "Dear Supervisor, I am highly interested in your NLP project as I have experience with BERT models.",
        "Sir, I would like to do my final year design project on low-power VLSI design. Please consider me.",
        "I have a CGPA of 3.8 and background in SCADA systems. I want to work under your esteemed supervision.",
        "Dear Teacher, your paper on Smart Agriculture inspired me. I want to build the LoRa module under you.",
        "Hello Sir, I have a deep interest in Quantum Cryptography. I have done several online courses on it.",
        "Ma'am, I am seeking supervision for my thesis on Eco-Building designs. Here is my profile summary.",
        "Sir, I have practical experience in building SLAM robots. I want to contribute to your robotics lab.",
        "Dear Sir, I am writing to express my interest in working under you for my CSE 400 thesis. Thanks."
    ]
    
    applications = []
    for i in range(20):
        student = students[i]
        project = projects[i % len(projects)]
        teacher = project.teacher
        message = application_messages[i % len(application_messages)]
        
        # Avoid violating our trigger constraint: we must only have ONE Accepted application per student!
        # Thus, let's make only 3 students "Accepted" and the rest "Pending" or "Rejected"!
        if i < 3:
            status = "Accepted"
        elif i < 15:
            status = "Pending"
        else:
            status = "Rejected"
            
        app = Application.objects.create(
            project=project if (i % 3 != 0) else None,
            student=student,
            teacher=teacher,
            message=message,
            status=status
        )
        applications.append(app)
    print(f"Created {len(applications)} supervision applications.")

    # 8. Populate Messages (20 messages)
    message_texts = [
        "Hello Sir, did you have a chance to review my collaboration request?",
        "Yes, I reviewed it. Your CGPA is impressive. Let's meet tomorrow at 10 AM.",
        "Thank you! I will be at your room on time.",
        "Perfect, bring a printed copy of your CV.",
        "Sure, I will bring it with me.",
        "Hello Ma'am, do you have any open spots for NLP research this semester?",
        "Hi! I currently have one open spot. Please apply through the portal.",
        "I have submitted the application. Looking forward to your response.",
        "Great, I will evaluate your skills and let you know by next week.",
        "Understood. Thanks for your time!",
        "Sir, I updated my research interests with IoT and sensor networks.",
        "Excellent. That fits our upcoming smart grid project.",
        "Can I read some papers before our meeting?",
        "Yes, read the IEEE 2024 paper on microgrid active stability.",
        "I will download and read it today. Thank you, sir.",
        "Ma'am, when is the deadline to lock our thesis supervisor?",
        "It's by the end of this month. Make sure to finalize soon.",
        "I will apply to your blockchain opportunity today.",
        "Sure, I will review all student applications together this Friday.",
        "Perfect. Have a good day, ma'am!"
    ]
    
    messages = []
    for i in range(20):
        if i % 2 == 0:
            sender = students[i % len(students)].user
            receiver = teachers[i % len(teachers)].user
        else:
            sender = teachers[i % len(teachers)].user
            receiver = students[i % len(students)].user
            
        msg = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message_text=message_texts[i]
        )
        messages.append(msg)
    print(f"Created {len(messages)} direct messages.")

    print("\nDatabase seeding completed successfully!")
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Departments: {Department.objects.count()}")
    print(f"Total Students: {Student.objects.count()}")
    print(f"Total Teachers: {Teacher.objects.count()}")
    print(f"Total Projects: {Project.objects.count()}")
    print(f"Total Applications: {Application.objects.count()}")
    print(f"Total Messages: {Message.objects.count()}")

if __name__ == '__main__':
    seed_database()
