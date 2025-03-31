from flask import Flask, request, jsonify, render_template, session
from markupsafe import Markup
import re
from typing import List, Dict, Union
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'cuz_chatbot_secret_key_2023'

class CUZChatbot:
    def __init__(self):
        self.knowledge_base = {
            "general": {
                "welcome": "Welcome to the Catholic University of Zimbabwe (CUZ)! We look forward to welcoming you and are here to provide the information and tools to help you make the most of this opportunity, get involved with our University community, and get to know your new home.",
                "history": "The Catholic University of Zimbabwe was established to address the need for a Catholic institution of higher education in Zimbabwe. Spearheaded by lay Catholics, predominantly Kutama College alumni and the Kutama Old Boys Association (KOBA), they were later joined by Friends of the Catholic University of Zimbabwe (FOCUZ). It was officially founded on 20 August 1998 through Statutory Instrument 268, Proclamation 49 of 1998, opening its doors on 25 February 1999 with 41 students.",
                "founders": "Founded by lay Catholics, primarily Kutama College alumni and KOBA members, later joined by FOCUZ. Initial executive committee (1991) included Prof. G.P. Kahari, Mr. Herbert Munangatire, Mr. L.C. Vambe, Mr. P.H.J. Arnold, Dr. L. Tsumba, Mr. L.C. Mbanga, Fr. A.B. Berridge SJ, Prof. S.J. Nondo, Prof. T.O. McLoughlin, Prof. A.J. Chennels. Patrons: late Archbishop Patrick Chakaipa and late President Robert Mugabe.",
                "vision": "To be the University of choice for Inclusive, holistic and adaptive Education in a Christian environment.",
                "mission": "CUZ provides inclusive, holistic and adaptive education in a Christian environment through its teaching, research, innovation, industrialization, and service programs to all, irrespective of religion, nationality, or any other designation.",
                "values": "Ethical behavior, Inclusivity, Collegiality, Commitment, Service, Excellence, Innovation, Adaptation",
                "contact": "Main Campus: 18443, Cranborne Avenue, Hatfield, Harare | Email: info@cuz.ac.zw | Phone: +263868 800 2370 | Website: www.cuz.ac.zw",
                "locations": {
                    "harare": "18443 Cranborne Avenue, Hatfield | Phone: 0242 570 570/169, +263868 800 2370",
                    "bulawayo": "Cnr 4th Avenue/Jason Moyo Street | Phone: 0771 784 923",
                    "mutare": "2nd Floor Oasis Mall, 12 Herbert Chitepo Street | Phone: 0202 062 604, 0772 650 751",
                    "gokwe": "Shingai Training Centre | Phone: 0259 2994, 0776 018 200",
                    "chinhoyi": "National Tyre Services, 40 Magamba Way | Phone: 0672 123 281, 0775 350 254",
                    "masvingo": "c/o Caritas Zimbabwe, 14 Simon Muzenda Street | Phone: 0776 177 822",
                    "gweru": "Cathedral Hall, Cnr Lobengula & 7th Street | Phone: 0254 223 2896, 0777 649 394",
                    "chishawasha": "Chishawasha Seminary, Off Enterprise Road, Harare"
                },
                "founding_principles": "FOCUZ aimed to create a university upholding Catholic principles, moral integrity, academic excellence, and a spirit of service, producing graduates with ethical values and societal impact.",
                "early_growth": "Opened 25 Feb 1999 with 41 BBM&IT students. Aug 2000: 13 BA students admitted. First graduation 5 Feb 2004: 45 graduates (36 BBM&IT, 5 BA General, 4 BA Honours).",
            },
            "admissions": {
                "general_requirements": "Undergraduate: 5 'O' Level passes (including English and Mathematics) and 2 'A' Level passes. Mature entry: 25+ years, 5 'O' Levels, relevant diploma/certificate, and work experience. Postgraduate: Varies by program, typically a relevant degree with 2.2 or better.",
                "process": "1. Submit application online\n2. Attach required documents\n3. Pay application fee\n4. Await decision (4-6 weeks)",
                "deadlines": "Applications typically close 1-2 months before semester start (August and January)",
                "fees": "Application fee: $20-$30 USD | Tuition: ~$800-$1,200/year (undergraduate), ~$1,500-$2,000/year (postgraduate)",
                "contact": "Email: admissions@cuz.ac.zw | Phone: +263868 800 2370"
            },
            "faculties": {
                "commerce_innovation_technology": {
                    "dean": "Dr. Cletos Garatsa (PhD Management Sciences, Durban University of Technology; MBL, University of South Africa)",
                    "overview": "Since 1999, FCIT blends business and technology, offering Accounting, Finance, Marketing, Business Management, and IT programs. Focuses on sustainable development, Education 5.0, and industry integration for the 4th Industrial Revolution.",
                    "research_mantra": "Life-changing research and innovation for the community and individuals around us.",
                    "undergraduate": {
                        "bbm_it": "Bachelor of Business Management and IT Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "finance": "Bachelor of Business Management in Finance Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "marketing": "Bachelor of Business Management in Marketing Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "accounting": "Bachelor of Accounting Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry"
                    },
                    "postgraduate": {
                        "mbm_it": "Master of Business Management and IT (1.5 years): Good honours degree in Business/IT",
                        "mba": "Master of Business Administration (2 years): Recognized degree plus 2 years work experience"
                    },
                    "diploma": {
                        "project_management": "Project Management, Monitoring and Evaluation (1 year): 5 'O' Levels (English, Maths), 'A' Levels or work experience an advantage",
                        "financial_admin": "Financial Administration (1 year): 5 'O' Levels (English, Maths), 'A' Levels or work experience an advantage"
                    },
                    "short_courses": {
                        "project_management": "Project Management, Monitoring and Evaluation (6 months): 5 'O' Levels (English), one weekend/month",
                        "business_admin": "Business Administration (6 months): 5 'O' Levels (English), one weekend/month",
                        "research_methodology": "Applied Research Methodology (6 months): 5 'O' Levels (English), one weekend/month",
                        "mobile_dev": "Mobile Application Development (6 months): 5 'O' Levels (English), one weekend/month",
                        "hospitality": "Hospitality and Tourism Management (6 months): 5 'O' Levels (English), one weekend/month",
                        "digital_marketing": "Digital Marketing (6 months): 5 'O' Levels (English), one weekend/month",
                        "standardisation": "Certificate in Standardisation (with SAZ) (6 months): 5 'O' Levels (English), one weekend/month",
                        "beekeeping": "Beekeeping Entrepreneurship (3 months): 5 'O' Levels (English)"
                    },
                    "contact": "Email: fcit@cuz.ac.zw | WhatsApp: +263780008886"
                },
                "education_social_sciences_humanities": {
                    "dean": "Dr. Vimbisai Nhundu (PhD, MEd University of Alberta; MTh University of Botswana; BA University of Zimbabwe)",
                    "overview": "Formed in 2021 from merging Education (est. 2019) and Humanities (est. 2000), FESSH focuses on Education 5.0, Vision 2030, and SDGs. Offers Education, Social Sciences, and Humanities programs with Erasmus+ mobility since 2022.",
                    "postgraduate": {
                        "dev_practice": "Master in Development Practice & Management (1.5 years): Relevant degree, 2.2 or better",
                        "climate_change": "Master in Climate Change & Sustainable Development (1.5 years): Relevant degree, 2.2 or better",
                        "conflict_peace": "Master of Science in Applied Conflict, Transformation & Peace Building (2 years): Relevant degree, 2.2 or better",
                        "pgde": "Post-Graduate Diploma in Education (1.5 years): Relevant degree, block release"
                    },
                    "undergraduate": {
                        "dev_studies": "Bachelor of Social Science in Development Studies Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "ba_dual": "Bachelor of Arts Dual (English/Media Studies or Geography/Disaster Management) Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "env_sciences": "Bachelor in Environmental Sciences Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "rural_dev": "Bachelor in Rural Development & Food Security Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "child_protection": "Bachelor in Child Protection and Care Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "peace_conflict": "Bachelor in Sustainable Peace & Conflict Transformation Honours (4 years): 5 'O' Levels (English, Maths), 2 'A' Levels or mature entry",
                        "ecd": "Bachelor of Education in Early Childhood Development Honours (4 years pre-service, 2 years in-service): 5 'O' Levels (English, Maths), 2 'A' Levels or diploma",
                        "primary_ed": "Bachelor of Education in Primary Education Honours (4 years pre-service, 2 years in-service): 5 'O' Levels (English, Maths), 2 'A' Levels or diploma",
                        "science_design": "Bachelor of Education in Science, Design and Technology (4 years pre-service, 2 years in-service): 5 'O' Levels (English, Science, Maths), 2 'A' Levels or diploma",
                        "secondary_stem": "Bachelor of Secondary Education in STEM Honours (4 years pre-service, 2 years in-service): 5 'O' Levels (English, Science, Maths), 2 'A' Levels or diploma",
                        "secondary_commercials": "Bachelor of Secondary Education in Commercials Honours (4 years pre-service, 2 years in-service): 5 'O' Levels (English, Commercial), 2 'A' Levels or diploma"
                    },
                    "diploma": {
                        "child_safeguarding": "Diploma in Child Safeguarding, Protection and Care (2 years): 5 'O' Levels (English)",
                        "special_needs": "Diploma in Special Needs Education (2 years): 5 'O' Levels (English)"
                    },
                    "short_courses": {
                        "gis": "Geographic Information Systems & Remote Sensing (6 months): 5 'O' Levels (English), one weekend/month",
                        "disaster_mgmt": "Disaster Management (6 months): 5 'O' Levels (English), one weekend/month",
                        "ngo_mgmt": "NGO Management (6 months): 5 'O' Levels (English), one weekend/month",
                        "child_safeguarding": "Child Safeguarding, Protection & Care (6 months): 5 'O' Levels (English), one weekend/month",
                        "counselling": "Counselling Psychology (6 months): 5 'O' Levels (English), one weekend/month",
                        "caregiving": "Caregiving Standards and Practices (6 months): 5 'O' Levels (English), one weekend/month",
                        "resource_gov": "Resource Governance & Environmental Management (6 months): 5 'O' Levels (English), one weekend/month",
                        "community_dev": "Community Development (6 months): 5 'O' Levels (English), one weekend/month",
                        "rural_dev": "Rural Development & Sustainable Food Security (6 months): 5 'O' Levels (English), one weekend/month",
                        "climate_change": "Climate Change (6 months): 5 'O' Levels (English), one weekend/month",
                        "sustainable_disaster": "Sustainable Disaster Management (6 months): 5 'O' Levels (English), one weekend/month",
                        "entrepreneurship": "Entrepreneurship, Value Addition & Beneficiation (6 months): 5 'O' Levels (English), one weekend/month",
                        "drug_abuse": "Drug & Substance Abuse Management (6 months): 5 'O' Levels (English), one weekend/month",
                        "ethics": "Ethics & Humanitarian Standards in Programming (6 months): 5 'O' Levels (English), one weekend/month",
                        "research": "Applied Social Science Research Methodology (6 months): 5 'O' Levels (English), one weekend/month",
                        "caregiving_vulnerable": "Caregiving Standards & Practices (Children & Vulnerable Adults) (6 months): 5 'O' Levels (English), one weekend/month",
                        "sign_language": "Sign Language for Beginners (3 months): 5 'O' Levels (English), one weekend/month",
                        "tech_teaching": "Technology Enhanced Teaching and Learning (6 months): 5 'O' Levels (English), one weekend/month",
                        "social_work": "Social Work (1 year): 5 'O' Levels (English), one weekend/month"
                    },
                    "contact": "Email: fessh@cuz.ac.zw | WhatsApp: +263784042292"
                },
                "theology_ethics_religious_philosophy": {
                    "dean": "Dr. Julias Togarepi (PhD, MTh, BTh, PGDE)",
                    "overview": "Founded 2019, rebranded TERP in 2020. Offers theology, ethics, religious studies, and philosophy programs, focusing on practical Christianity, inculturation, and social transformation.",
                    "vision": "Advancing research, education, and social transformation through theology, spirituality, social communication, youth ministry, and catechetics.",
                    "mission": "Proclaiming the Gospel, training educators/spiritual leaders, and fostering contextual theology relevant to Zimbabwe and Africa.",
                    "undergraduate": {
                        "theology": "Bachelor of Theology Honours (4 years): 5 'O' Levels (English), 2 'A' Levels or mature entry",
                        "special_theology": "Special Honours in Theology (2 years): For priests with Diploma in Theology from Chishawasha Seminary"
                    },
                    "postgraduate": {
                        "m_theology": "Master’s in Theology (2 years, specializations: Biblical, Systematic, Moral, Church History, Pastoral): Upper second honours in Theology/related field",
                        "conflict_peace": "Master of Science in Applied Conflict, Transformation & Peace Building (2 years): Relevant degree, 2.2 or better"
                    },
                    "diploma": {
                        "chaplaincy": "Diploma in Chaplaincy (2 years): 5 'O' Levels (English)",
                        "peace_building": "Diploma in Peace Building Studies & Conflict Management (1.5 years): 5 'O' Levels (English)",
                        "catechetical": "Diploma in Catechetical Studies (1.5 years): 5 'O' Levels (English)",
                        "counselling": "Diploma in Counselling & Community Mental Health (2 years): 5 'O' Levels (English)"
                    },
                    "short_courses": {
                        "chaplaincy": "Chaplaincy (6 months): 5 'O' Levels (English), one weekend/month",
                        "church_admin": "Church Administration and Leadership (6 months): 5 'O' Levels (English), one weekend/month"
                    },
                    "contact": "Email: terp@cuz.ac.zw | WhatsApp: +263784042292"
                }
            },
            "strategic_plan": {
                "pillar1": "Grow Academic Programmes (2024-2028): Expand and consolidate programs, devise strategies for approved programs, and introduce new ones.",
                "pillar2": "Grow Infrastructure (2024-2028): Complete construction (chapel, teaching blocks, sports facilities), procure equipment, build hostels, and improve campus ambiance.",
                "pillar3": "Institutionalise Quality Performance (2024-2028): Consolidate QA structures, extend QA processes to all campuses, include QA in annual plans.",
                "pillar4": "Holistic Quality Experience (2024-2028): Provide sports, social occasions, and psycho-social-spiritual support for students and staff.",
                "pillar5": "Staff Retention (2024-2028): Improve conditions, academic promotions, psycho-social-spiritual welfare, and sense of belonging."
            },
            "quality_assurance": {
                "director": "Dr. Fine Masimba (PhD Information Systems, Vaal University of Technology; MSc, BSc Hons Information Systems, MSU)",
                "overview": "Est. 2023, the Quality Assurance Directorate ensures high academic and operational standards through evaluation, monitoring, and stakeholder feedback, aligning with national and international benchmarks.",
                "contact": "Email: qa@cuz.ac.zw | Phone: +263868 800 2370"
            },
            "faqs": {
                "when_opened": "25 February 1999 with 41 students",
                "first_graduation": "5 February 2004 with 45 graduates",
                "campuses": "8 campuses: Harare, Bulawayo, Mutare, Gokwe, Chinhoyi, Masvingo, Gweru, Chishawasha",
                "distance_learning": "Available for some programs (e.g., PGDE) through block release",
                "international_students": "Welcome with valid passport, academic certificates, and student visa"
            }
        }

        self.stop_words = set(stopwords.words('english'))
        self.contact_prompt = "For further details, contact the office at: Email: info@cuz.ac.zw | Phone: +263868 800 2370 | Website: www.cuz.ac.zw"
        self.capabilities = [
            "Provide information about CUZ programs and courses",
            "Explain admission requirements and processes",
            "Share details about faculties and departments",
            "Answer frequently asked questions",
            "Give contact information for different campuses",
            "Detail the university's history, vision, and strategic plans",
            "Describe quality assurance initiatives"
        ]

        self.intent_map = {
            "faculty": "faculties",
            "faculties": "faculties",
            "department": "faculties",
            "admission": "admissions",
            "admissions": "admissions",
            "program": "faculties",
            "programs": "faculties",
            "service": "services",
            "services": "services",
            "faq": "faqs",
            "faqs": "faqs",
            "strategy": "strategic_plan",
            "strategic": "strategic_plan",
            "quality": "quality_assurance",
            "qa": "quality_assurance"
        }

    def preprocess_text(self, text: str) -> List[str]:
        text = text.lower().translate(str.maketrans("", "", string.punctuation))
        tokens = word_tokenize(text)
        return [token for token in tokens if token not in self.stop_words]

    def clean_response_text(self, text: str) -> str:
        text = str(text).replace('{', '').replace('}', '').replace("'", "")
        return re.sub(r"([a-z])_([a-z])", r"\1 \2", text)

    def format_program_list(self, programs_dict: dict) -> str:
        formatted = "<ul>"
        for program_name, program_details in programs_dict.items():
            cleaned_name = self.clean_response_text(program_name.replace('_', ' ').title())
            cleaned_details = self.clean_response_text(program_details)
            formatted += f"<li><strong>{cleaned_name}:</strong> {cleaned_details}</li>"
        return formatted + "</ul>"

    def generate_category_response(self, category: str) -> str:
        response = f"<h2>{category.title()}</h2>"
        category_data = self.knowledge_base[category]

        if category == "faculties":
            for faculty_name, faculty_data in category_data.items():
                response += f"<h3>{self.clean_response_text(faculty_name).title()}</h3><ul>"
                for key, value in faculty_data.items():
                    if isinstance(value, dict):
                        response += f"<li><strong>{key.title()}:</strong> {self.format_program_list(value)}</li>"
                    else:
                        response += f"<li><strong>{key.title()}:</strong> {self.clean_response_text(value)}</li>"
                response += "</ul>"
        else:
            for key, value in category_data.items():
                if isinstance(value, dict):
                    response += f"<h3>{key.title()}:</h3><ul>"
                    for sub_key, sub_value in value.items():
                        response += f"<li><strong>{sub_key.title()}:</strong> {self.clean_response_text(sub_value)}</li>"
                    response += "</ul>"
                else:
                    response += f"<p><strong>{key.title()}:</strong> {self.clean_response_text(value)}</p>"
        return response

    def search_knowledge_base(self, tokens: List[str]) -> str:
        if 'awaiting_confirmation' in session:
            if "yes" in tokens:
                category = session.pop('awaiting_confirmation')
                return self.generate_category_response(category)
            elif "no" in tokens:
                session.pop('awaiting_confirmation')
                return "<p>Okay, what would you like to know about CUZ?</p>"
            else:
                session.pop('awaiting_confirmation', None)

        response = ""
        for token in tokens:
            if token in self.intent_map:
                category = self.intent_map[token]
                session['awaiting_confirmation'] = category
                return f"<p>Did you mean information about {category}? If yes, type 'yes'. If not, type 'no'.</p>"

            for category in self.knowledge_base:
                if token in self.knowledge_base[category]:
                    if isinstance(self.knowledge_base[category][token], dict):
                        response += f"<h3>{token.title()}:</h3><ul>"
                        for key, value in self.knowledge_base[category][token].items():
                            response += f"<li><strong>{key.title()}:</strong> {self.clean_response_text(value)}</li>"
                        response += "</ul>"
                    else:
                        response += f"<p><strong>{token.title()}:</strong> {self.clean_response_text(self.knowledge_base[category][token])}</p>"
                    return response

            for faculty in self.knowledge_base["faculties"]:
                if token == faculty or token in faculty:
                    faculty_data = self.knowledge_base["faculties"][faculty]
                    response += f"<h3>{self.clean_response_text(faculty).title()}:</h3><ul>"
                    for key, value in faculty_data.items():
                        if isinstance(value, dict):
                            response += f"<li><strong>{key.title()}:</strong> {self.format_program_list(value)}</li>"
                        else:
                            response += f"<li><strong>{key.title()}:</strong> {self.clean_response_text(value)}</li>"
                    response += "</ul>"
                    return response

        return f"<p>Sorry, I couldn't find info about '{' '.join(tokens)}'. What else can I help you with?</p>"

    def get_time_of_day(self) -> str:
        hour = datetime.now().hour
        if 5 <= hour < 12: return "Good morning"
        if 12 <= hour < 17: return "Good afternoon"
        if 17 <= hour < 21: return "Good evening"
        return "Hello"

    def generate_personalized_greeting(self) -> str:
        name = session.get('user_name', 'Friend')
        time_of_day = self.get_time_of_day()
        greeting = f"""
        <div class="greeting-message">
            <p>{time_of_day}, {name}! Welcome to Catholic University of Zimbabwe's chatbot.</p>
            <p>I can help you with:</p>
            <ul class="capabilities-list">
                <li>Provide information about CUZ programs and courses</li>
                <li>Explain admission requirements and processes</li>
                <li>Share details about faculties and departments</li>
                <li>Answer frequently asked questions</li>
                <li>Give contact information for different campuses</li>
                <li>Detail the university's history, vision, and strategic plans</li>
                <li>Describe quality assurance initiatives</li>
            </ul>
            <p class="prompt-text">What would you like to know today?</p>
        </div>
        """
        return Markup(' '.join(greeting.split()))

    def get_response(self, query: str) -> Dict[str, Union[str, bool]]:
        response = {'text': '', 'ask_name': False}
        if not query.strip():
            response['text'] = "<p>Please ask me something about CUZ!</p>"
            return response

        tokens = self.preprocess_text(query)
        if 'awaiting_name' in session:
            if query.strip():
                session['user_name'] = query.strip()
                session.pop('awaiting_name', None)
                response['text'] = self.generate_personalized_greeting()
            else:
                response['text'] = "<p>I didn't catch your name. Could you please tell me your name?</p>"
                response['ask_name'] = True
            return response

        if any(token in ["hello", "hi", "hey", "welcome"] for token in tokens):
            if 'user_name' not in session:
                session['awaiting_name'] = True
                response['text'] = "<p>Welcome to CUZ Chatbot! What's your name?</p>"
                response['ask_name'] = True
            else:
                response['text'] = self.generate_personalized_greeting()
            return response

        if any(token in ["bye", "goodbye", "exit", "quit"] for token in tokens):
            name = session.get('user_name', '')
            response['text'] = f"<p>Goodbye{f', {name}' if name else ''}! Come back anytime.</p>"
            return response

        kb_response = self.search_knowledge_base(tokens)
        response['text'] = kb_response + f"<p>{self.contact_prompt}</p>"
        return response

# Initialize chatbot
chatbot = CUZChatbot()

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '').strip()
        print(f"Received input: '{user_input}'")  # Debug log
        response = chatbot.get_response(user_input)
        print(f"Response: '{response['text']}'")  # Debug log
        return jsonify(response)
    except Exception as e:
        return jsonify({'text': f"<p>Sorry, an error occurred: {str(e)}</p>", 'ask_name': False})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)