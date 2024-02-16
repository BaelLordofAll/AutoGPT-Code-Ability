from codex.common.ai_block import (
    AIBlock,
    Indentifiers,
    ValidatedResponse,
    ValidationError,
)
from codex.prompts.claude.requirements.NestJSDocs import (
    NEST_JS_CRUD_GEN,
    NEST_JS_FIRST_STEPS,
    NEST_JS_MODULES,
    NEST_JS_SQL,
)
from codex.requirements.model import ModuleResponse


class ModuleGenerationBlock(AIBlock):
    """
    This is a block that handles, calling the LLM, validating the response,
    storing llm calls, and returning the response to the user

    """

    # The name of the prompt template folder in codex/prompts/{model}
    prompt_template_name = "requirements/module"
    # Model to use for the LLM
    model = "gpt-4-0125-preview"
    # Should we force the LLM to reply in JSON
    is_json_response = True
    # If we are using is_json_response, what is the response model
    pydantic_object = ModuleResponse

    def validate(
        self, invoke_params: dict, response: ValidatedResponse
    ) -> ValidatedResponse:
        """
        The validation logic for the response. In this case its really simple as we
        are just validating the response is a Clarification model. However, in the other
        blocks this is much more complex. If validation failes it triggers a retry.
        """
        try:
            model = ModuleResponse.model_validate_json(response.response, strict=False)
            response.response = model
        except Exception as e:
            raise ValidationError(f"Error validating response: {e}")

        return response

    async def create_item(
        self, ids: Indentifiers, validated_response: ValidatedResponse
    ):
        """
        This is where we would store the response in the database

        Atm I don't have a database model to store QnA responses, but we can add one
        """
        pass


if __name__ == "__main__":
    """
    This is a simple test to run the block
    """
    from asyncio import run

    from openai import OpenAI
    from prisma import Prisma

    ids = Indentifiers(user_id=1, app_id=1)
    db_client = Prisma(auto_register=True)
    oai = OpenAI()

    task: str = "'The Tutor App is an app designed for tutors to manage their clients, schedules, and invoices. \n\nIt must support both the client and tutor scheduling, rescheduling and canceling appointments, and sending invoices after the appointment has passed.\n\nClients can sign up with OAuth2 or with traditional sign-in authentication. If they sign up with traditional authentication, it must be safe and secure. There will need to be password reset and login capabilities. \n\nThere will need to be authorization for identifying clients vs the tutor.\n\nAdditionally, it will have proper management of financials, including invoice management and payment tracking. This includes things like paid/failed invoice notifications, unpaid invoice follow-up, summarizing d/w/m/y income, and generating reports.'"
    project_description: str = "The Tutor App is an application designed to help tutors manage their tutoring business and clients manage their tutoring sessions. The key users are both tutors and clients. Tutors need features to set availability, manage clients, schedule sessions, send invoices and track payments. Clients need to find tutors, book and manage appointments, communicate with tutors, and pay invoices. Core features like user accounts, authentication, notifications span both groups. But the functionality aims to let tutors run their services smoothly while giving clients control over their tutoring.'"
    product_description: str = "TutorMate is a dedicated app designed to streamline the management of tutoring services. It serves as a centralized platform for tutors to manage clients, appointments, and invoices with ease. For clients, it offers a seamless way to book, reschedule, or cancel sessions, and manage payments. TutorMate supports OAuth2 and traditional sign-in authentication for enhanced security. It features robust password reset and login capabilities, along with distinct authorization methods for distinguishing between tutors and clients. Financial management is a cornerstone of TutorMate, including invoice generation, payment tracking, income summary reports, and notification systems for payment status. The app is developed with scalability and international use in mind, automatically adjusting for different time zones and supporting secure financial transactions."
    joint_q_and_a: str = """
'- "Do we need a front end for this: "The Tutor App is an application designed to help tutors manage their tutoring business and clients manage their tutoring sessions. The key users are both tutors and clients. Tutors need features to set availability, manage clients, schedule sessions, send invoices and track payments. Clients need to find tutors, book and manage appointments, communicate with tutors, and pay invoices. Core features like user accounts, authentication, notifications span both groups. But the functionality aims to let tutors run their services smoothly while giving clients control over their tutoring."": "Yes" : Reasoning: "Considering the requirements specified for the Tutor App, a front end is essential. The app aims to provide an accessible interface for two distinct user types (tutors and clients), each with specific needs and interactions with the application. Tutors need to manage various aspects of their tutoring business, including setting availability, managing clients, and handling finances. Clients, on the other hand, need to easily find tutors, book appointments, and communicate. These interactions require a user-friendly, interactive front end that makes these tasks efficient and intuitive. Moreover, features like authentication and notifications imply direct, real-time engagement with the app, reinforcing the need for a well-designed front end. Without it, achieving the application\'s goals of streamlining the business and learning experience would be impractical, if not impossible."\n- "Who is the expected user of this: "The Tutor App is an application designed to help tutors manage their tutoring business and clients manage their tutoring sessions. The key users are both tutors and clients. Tutors need features to set availability, manage clients, schedule sessions, send invoices and track payments. Clients need to find tutors, book and manage appointments, communicate with tutors, and pay invoices. Core features like user accounts, authentication, notifications span both groups. But the functionality aims to let tutors run their services smoothly while giving clients control over their tutoring."": "Tutors and clients" : Reasoning: "The Tutor App serves two main user personas: tutors and clients. For tutors, the app functions as a comprehensive business management tool, enabling features like setting availability, managing client relations, scheduling, and handling finances. It’s designed to simplify the operational aspects of tutoring, allowing tutors to focus on delivering quality education. For clients, the app acts as a bridge to access tutoring services. They can effortlessly search for tutors, book and manage sessions, and handle payments. This dual approach caters to the full lifecycle of tutoring services, from discovery and learning to payment. The inclusion of core features like user accounts, authentication, and notifications for both groups emphasizes the app’s goal to foster seamless interaction between tutors and clients, highlighting its commitment to creating a beneficial environment for teaching and learning."\n- "What is the skill level of the expected user of this: "The Tutor App is an application designed to help tutors manage their tutoring business and clients manage their tutoring sessions. The key users are both tutors and clients. Tutors need features to set availability, manage clients, schedule sessions, send invoices and track payments. Clients need to find tutors, book and manage appointments, communicate with tutors, and pay invoices. Core features like user accounts, authentication, notifications span both groups. But the functionality aims to let tutors run their services smoothly while giving clients control over their tutoring."": "Varied" : Reasoning: "Considering the description of the Tutor App, it\'s clear that the expected user base consists of two main personas: tutors and clients. Each of these personas has different roles and objectives within the app, which in turn implies different levels of technology proficiency. Tutors are expected to manage more complex tasks related to running a business such as setting their availability, managing client information, scheduling sessions, and managing finances. On the other hand, clients are primarily looking to find tutors, book and manage appointments, and make payments. Given these tasks, it’s reasonable to assume a variance in technical skill levels among the users. Tutors might possess a moderate to high level of technological proficiency, given their need to manage multiple aspects of their tutoring business through the app. Clients, however, may range from low to high technological proficiency, as their primary interaction with the app involves searching, booking, and communicating. The app should therefore be designed to be intuitive and accessible, catering to the widest possible range of user skill levels to ensure both tutors and clients can navigate and utilize its features effectively."\n- "What types of notifications should the system support for both tutors and clients, and through what channels (SMS, email, in-app)?": "Support email and in-app notifications for all users, with an optional SMS feature based on budget and user preferences." : Reasoning: "Notifications are vital for keeping users engaged and informed. Understanding the types and channels of notifications can shape the development of notification services and APIs."\n- "How should the app handle time zones for scheduling appointments, considering users might be in different regions?": "Implement functionality to adjust and display time based on the user’s local time zone, using UTC as the standard for backend storage." : Reasoning: "Properly handling time zones is crucial for a scheduling app to avoid confusion and missed appointments."\n- "What level of customization will tutors have over their profile and scheduling settings?": "Tutors can customize their profile with essential business information and manage availability settings to enhance user experience without overcomplicating the UI/UX." : Reasoning: "Enhancing tutor profiles with customization options can improve match rates but may increase complexity."\n- "What specific security measures will be implemented for authentication, especially for traditional sign-ins?": "Secure traditional sign-ins with strong password requirements, hashed password storage, SSL for data in transit, and evaluate the need for 2FA based on user feedback." : Reasoning: "With options for OAuth2 and traditional sign-ins, ensuring security for passwords and user data is imperative."\n- "How should the app facilitate communication between tutors and clients?": "Implement an in-app messaging system for real-time communication, ensuring it is secure, user-friendly, and privacy-compliant." : Reasoning: "Direct communication is a key feature for scheduling and updates. Determining the channels and mechanisms is crucial for defining the scope of development."\n- "Which payment gateways or services will the app integrate with for handling invoices and payments?": "Integrate with reputable payment services like Stripe and PayPal, ensuring the integration is secure and user-friendly." : Reasoning: "Choosing the right payment gateway is essential for simplifying financial transactions and ensuring user trust."\n- "What reporting features are essential for tutors to manage their finances within the app?": "Implement essential reporting features for financial management, including income summaries, invoice tracking, and expense reports, with room for customization." : Reasoning: "Financial management tools are key for tutors to track their business. Identifying crucial reporting features will guide the design of this functionality."\n- "Will there be a rating or feedback system for tutors and clients to assess their experiences?": "A rating and feedback system for both tutors and clients will be implemented, designed to be fair, transparent, and resistant to manipulation." : Reasoning: "A feedback system can enhance trust and quality on the platform, but it requires careful consideration to be balanced and fair."\n- "How will the app accommodate users with disabilities or those requiring assistive technologies?": "The app will be designed with accessibility in mind, complying with standard guidelines and including features that support users with various needs." : Reasoning: "Accessibility is a fundamental aspect of app design, especially for a diverse user base. Understanding these requirements early aids compliance and inclusivity."\n- "What kind of support or documentation will be provided to users to facilitate onboarding and troubleshooting?": "Provide detailed documentation, onboarding tutorials, and an easily navigable FAQ section to ensure users have all the resources they need." : Reasoning: "Effective onboarding and accessible support materials can dramatically improve user satisfaction and reduce support requests."\n'
    """
    thoughts: str = """
'\n\nHuman: Your task is to "The Tutor App is an app designed for tutors to manage their clients, schedules, and invoices. \n\nIt must support both the client and tutor scheduling, rescheduling and canceling appointments, and sending invoices after the appointment has passed.\n\nClients can sign up with OAuth2 or with traditional sign-in authentication. If they sign up with traditional authentication, it must be safe and secure. There will need to be password reset and login capabilities. \n\nThere will need to be authorization for identifying clients vs the tutor.\n\nAdditionally, it will have proper management of financials, including invoice management and payment tracking. This includes things like paid/failed invoice notifications, unpaid invoice follow-up, summarizing d/w/m/y income, and generating reports."\n\nAnswer as an expert product owner.\n\nyour memory is based on a google like search. When you want more information send search:<query> and I\'ll send you back the reply.\n\nyou can ask the user questions by sending ask:<query> and I\'ll send you back the reply. Make sure to ask broad questions that help guide your understanding\n\nWhen you feel you have finished getting the info you need or are confident it\'s not there, summarize the memory you\'ve built and send finished:<summary>. make sure you don\'t reply anything before the "finished:<summary>" or it will confuse the human\n\nOnly reply with one message at a time so that the user isn\'t overwhelmed.\n\nOnly reply with the specified tags.\n\nAssistant: \nask: Who is the primary user for this application?\n\nHuman:Unfortunately I do not have enough context to definitively state who the primary user for a particular application would be. Applications can have different target users depending on their purpose and functionality. Some things that could help determine the primary user could be:\n\n- What is the main purpose or function of the application? Different types of apps may target different audiences (e.g. gaming apps target gamers, productivity apps target professionals, etc.)\n\n- Who is the application designed for? The UI/UX design and features may give clues as to the intended user base.\n\n- Who is the developer or company that created the application? Understanding their typical customer base could indicate who they had in mind as users.\n\n- What permissions and data does the app require or have access to? This could imply the expected user type based on what functionality is offered.\n\n- Are there any marketing materials or app descriptions that describe the target user base? Oftentimes there is explicit information on ideal users.\n\nWithout more context about which specific application you have in mind, I unfortunately cannot definitively name the expected primary user. Let me know if you can provide any additional details about the app and I\'m happy to try to make a more educated guess!\n\nAssistant:search: The Tutor App tutor schedule management clients invoices appointments OAuth2 sign-in authentication password reset login authorization identifying clients vs tutor financials invoice management payment tracking paid/failed invoice notifications unpaid invoice follow-up summarizing income reports\n\nHuman:Unfortunately I do not have enough context to provide specific feedback on features for a tutor scheduling and management app. However, some general capabilities that may be useful include:\n\n- User account management with sign-up, login, authentication, password reset, etc. Using a standard authorization protocol like OAuth 2.0 can simplify this.\n\n- Separate portals/views for tutors vs clients with appropriate functionality for each. Tutors need schedule/appointment management, client management, invoice/payment tracking, etc. Clients need to book, pay and manage appointments.\n\n- Client profiles/accounts to store info like name, contact details, billing info. This keeps client data organized and allows things like recurring appointments or billing.\n\n- Tutor calendar/availability management. Tutors need to indicate their availabilities and block off times they cannot take appointments.\n\n- Appointment management system - tutors and clients can add, edit, cancel, reschedule appointments. Notifications for upcoming sessions.\n\n- Invoicing system - automated invoice generation and tracking tied to appointments. Status indicators for paid/unpaid/failed payments. Reminders for unpaid invoices.\n\n- Payment processing and tracking against invoices. Recording payments as they come in and reconciling with invoices.\n\n- Financial/earnings reporting for tutors - reports on net earnings, paid invoices over time, appointment volume, etc. to analyze their tutoring business.\n\n- Notifications to both clients and tutors via email or SMS for unpaid invoices, appointment reminders/changes, etc. to improve engagement.\n\nLet me know if any specific features come to mind and I\'m happy to provide additional suggestions on how those could be implemented.\n\nAssistant:'
    """

    features_str: str = """[{"name": "Dual Authentication System", "thoughts": "Balancing security with ease of use is paramount. Offering both OAuth2 for those desiring quick access and a traditional sign-in for others emphasizes this.", "description": "A flexible authentication system allowing users to sign up and log in either via OAuth2 for seamless integration with existing accounts or through a secure, traditional sign-in process.", "considerations": "The need to implement stringent security measures, especially for the traditional sign-in, to protect user data.", "risks": "Potential complexity in maintaining two parallel systems and ensuring both are secure against breaches.", "needed_external_tools": "OAuth2 integration services, Secure password storage and hashing tools", "priority": "CRITICAL"}, {"name": "Comprehensive Scheduling System", "thoughts": "The core functionality that must cater to both setting and managing appointments by tutors and clients, including modifications and cancellations.", "description": "An intuitive scheduling interface that allows for the creation, rescheduling, and cancellation of appointments. This system supports real-time updates and notifications.", "considerations": "User experience should remain a priority, ensuring the system is intuitive for both clients and tutors.", "risks": "Synchronization issues leading to double bookings or missed appointments.", "needed_external_tools": "Calendar API services, Push notification services", "priority": "CRITICAL"}, {"name": "Advanced Financial Management", "thoughts": "Providing a detailed yet easy-to-navigate financial overview, including invoicing and payment tracking, is essential for tutor's business operations.", "description": "A robust financial management module for handling invoices, tracking payments, and following up on unpaid invoices. Features include financial summary reports for various time frames.", "considerations": "Ease of understanding and interaction for users with varying financial literacy.", "risks": "Complexity of financial data handling and ensuring accuracy in reports and summaries.", "needed_external_tools": "Invoice management software integration, Payment gateway services", "priority": "HIGH"}, {"name": "Role-Based Authorization", "thoughts": "Critical for differentiating access levels between tutors and clients to ensure both parties only access relevant data and functionalities.", "description": "An authorization framework that differentiates user roles, granting access permissions according to the user's role as a tutor or client.", "considerations": "Ensuring a seamless yet secure method of identifying and authorizing users based on their roles.", "risks": "Potential security vulnerabilities if role distinctions are not properly enforced.", "needed_external_tools": "Role-based access control (RBAC) systems", "priority": "HIGH"}]"""
    requirements_q_and_a_string: str = """'- "do we need db?": "Yes" : Reasoning: "Considering the need to store a vast amount of data like user profiles, schedules, invoices, and payments securely, a database is essential for organizing and managing this information efficiently."\n- "do we need an api for talking to a front end?": "Yes" : Reasoning: "Given the separation of concerns and the necessity to communicate data between the server and the client-side application seamlessly, an API serves as an essential medium for this interaction."\n- "do we need an api for talking to other services?": "Yes" : Reasoning: "For features like OAuth2 authentication, payment processing, and possibly other third-party services, having an API that allows our app to communicate with these external services is crucial."\n- "do we need an api for other services talking to us?": "Yes" : Reasoning: "To facilitate interoperability and integration with other platforms or services that might need to access our application\'s functionalities, we would require an API."\n- "do we need to issue api keys for other services to talk to us?": "Yes" : Reasoning: "To ensure secured access and interaction with our API, issuing API keys to third-party services allows us to control and monitor the API usage."\n- "do we need monitoring?": "Yes" : Reasoning: "Monitoring is essential to ensure the health, performance, and security of the application, helping in timely detection and resolution of potential issues."\n- "do we need internationalization?": "Yes" : Reasoning: "Anticipating a global user base and aiming for a broader reach necessitates the support for multiple languages and regional settings."\n- "do we need analytics?": "Yes" : Reasoning: "To understand user behaviour, measure performance, and guide data-driven decisions for future improvements, integrating analytics is vital."\n- "is there monetization?": "Yes" : Reasoning: "Considering the financial management aspect and the invoicing feature, monetization strategies like subscription models could be implemented to support the application\'s sustainability."\n- "is the monetization via a paywall or ads?": "Paywall" : Reasoning: "Given the professional context of the application for tutors and their clients, a paywall relying on subscriptions provides a more seamless, ad-free experience."\n- "does this require a subscription or a one-time purchase?": "Subscription" : Reasoning: "A subscription model aligns with the ongoing nature of tutoring services, offering continuous access and support to the features and updates."\n- "is the whole service monetized or only part?": "Part" : Reasoning: "It\'s reasonable to keep core functionalities behind a paywall while offering certain basic features for free to attract and onboard users before they commit to a subscription."\n- "is monetization implemented through authorization?": "Yes" : Reasoning: "Utilizing authorization to manage access based on subscription status enables a segmented approach to feature availability, aligning with the monetization strategy."\n- "do we need authentication?": "Yes" : Reasoning: "Authentication is fundamental to identifying users and ensuring data security, especially when managing personal and financial information."\n- "do we need authorization?": "Yes" : Reasoning: "Authorization is crucial for differentiating between user roles and controlling access to functionalities specific to tutors, clients, and possibly admin users."\n- "what authorization roles do we need?": "["Tutor", "Client", "Admin"]" : Reasoning: "Given the nature of the application, separating users into distinct roles ensures appropriate access and functionality tailored to their needs."\n'"""
    requirements_as_string: str = """'{"functional": [{"thoughts": "Considering security and user distinction is vital for protecting sensitive information and ensuring appropriate system access.", "name": "User Registration and Authentication", "description": "Enables tutors and clients to register and authenticate using OAuth2 or traditional sign-in methods, with distinct role identification."}, {"thoughts": "A core feature that requires a balance of flexibility and usability to cater to the scheduling needs of all users.", "name": "Appointment Scheduling", "description": "Allows tutors and clients to book, reschedule, or cancel appointments through a calendar interface, with automatic adjustment for time zones."}, {"thoughts": "Financial management is crucial for tutors; the system must provide accurate, timely, and secure handling of transactions.", "name": "Invoice Management", "description": "Automated invoice generation and management after sessions, including payment gateway integration for secure transactions."}, {"thoughts": "Keeping users informed in real time is essential for engagement and operational efficiency.", "name": "Real-time Notifications", "description": "Sends notifications for upcoming appointments, invoice statuses, and other relevant events through the app, email, or SMS."}, {"thoughts": "Data-driven insights can empower tutors to make informed decisions to enhance their services.", "name": "Reporting and Analytics", "description": "Generates comprehensive reports and analytics on income, client satisfaction, and session outcomes for tutors."}, {"thoughts": "Direct communication can resolve uncertainties, build rapport, and improve service satisfaction.", "name": "Direct Messaging System", "description": "Facilitates secure and private communication between tutors and clients within the app."}], "nonfunctional": [{"thoughts": "A non-negotiable aspect to protect user data and build trust.", "name": "Security and Compliance", "description": "Ensures data encryption, compliance with financial regulations, and robust authentication mechanisms."}, {"thoughts": "Anticipating growth is crucial for long-term success, necessitating a flexible and robust backend architecture.", "name": "Scalability", "description": "Designed to efficiently handle increasing loads, supporting user growth through scalable infrastructure."}, {"thoughts": "Performance impacts user satisfaction directly; thus, maintaining a swift and reliable system is essential.", "name": "Performance", "description": "Ensures quick response times and high availability to facilitate a seamless user experience."}, {"thoughts": "Given the varied tech-savviness of users, the interface must be accessible and easy to navigate.", "name": "Usability", "description": "Intuitive UI/UX design catering to users with intermediate technical skills, emphasizing ease of use."}, {"thoughts": "Flexibility in handling international contexts will ensure the app\'s broader applicability and user inclusiveness.", "name": "Internationalization", "description": "Supports different time zones and potentially multiple languages to cater to a global user base."}, {"thoughts": "Considering the global scope and sensitivity of data handled, compliance with privacy laws is crucial.", "name": "Data Privacy", "description": "Adheres to local and international data protection laws to safeguard personal and financial information."}]}'"""
    module_block = ModuleGenerationBlock(
        oai_client=oai,
    )

    async def run_ai() -> dict[str, ModuleResponse]:
        await db_client.connect()
        modules: ModuleResponse = await module_block.invoke(
            ids=ids,
            invoke_params={
                "NEST_JS_FIRST_STEPS": NEST_JS_FIRST_STEPS,
                "NEST_JS_MODULES": NEST_JS_MODULES,
                "NEST_JS_SQL": NEST_JS_SQL,
                "NEST_JS_CRUD_GEN": NEST_JS_CRUD_GEN,
                "product_description": product_description,
                "joint_q_and_a": joint_q_and_a,
                "requirements_q_and_a_string": requirements_q_and_a_string,
                "requirements": requirements_as_string,
            },
        )

        await db_client.disconnect()
        return {
            "modules": modules,
        }

    modules = run(run_ai())

    for key, item in modules.items():
        if isinstance(item, ModuleResponse):
            print(f"ModuleResponse {key}")
            print(f"\tThought General: {item.think_general}")
            print(f"\tThought Anti: {item.think_anti}")

            for m in item.modules:
                print(f"\t\tModule Name: {m.name}")
                print(f"\t\tModule Description: {m.description}")
                print(f"\t\tModule Requirements: {m.requirements}")
                print(f"\t\tModule Endpoints: {m.endpoints}")
                print(f"\t\tModule Related Modules: {m.related_modules}")

        else:
            print(f"????")
            breakpoint()

    # # If you want to test the block in an interactive environment
    # import IPython

    # IPython.embed()
    breakpoint()