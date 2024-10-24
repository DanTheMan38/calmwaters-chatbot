from flask import Flask, render_template, request, jsonify
import markdown

app = Flask(__name__)

# Define the FAQs as a list of dictionaries
faqs = [
    {
        "question": "What properties are available for rental?",
        "answer": """We offer a variety of properties to suit your needs, including cabins, apartments, and houses. Some of our featured properties include:

- **Clifftop Cabin**: A luxurious cabin with sea views, perfect for a tranquil getaway.
- **Wildside Cabin**: A cozy cabin nestled in nature, ideal for relaxation.
- **Rondebos Retreat**: A spacious farmhouse for families seeking peace and serenity.
- **Hill Penthouse Plett**: A penthouse apartment boasting breathtaking ocean views.
- **Hill Sea-View Apartment**: An elegant apartment with panoramic sea vistas.
- **Arrowood Apartment**: A comfortable apartment close to town and the beach.
- **Toplis Vista**: A large house with sea and mountain views, perfect for larger groups.
- **Keurbooms River Apartment**: A riverside apartment offering scenic views.
- **Dassen Eiland Home**: A charming home near the beach.
- **Panorama Seaview Flat**: An apartment with stunning sea views."""
    },
    {
        "question": "How can I book a property?",
        "answer": """You can book our properties through our website or via popular booking platforms such as Airbnb, Booking.com, and LekkeSlaap. Links to each property's listing are available on our website."""
    },
    {
        "question": "What amenities are available at the properties?",
        "answer": """Amenities vary by property but may include:

- **Comfort**: Air conditioning, heating, fans.
- **Entertainment**: Television, Wi-Fi access.
- **Kitchen**: Fully equipped kitchens with microwaves, dishwashers, coffee and tea facilities.
- **Laundry**: Washing machines, tumble dryers, irons.
- **Outdoor**: BBQ facilities, fireplaces, patios with views.
- **Extras**: Hairdryers, body wash, linens, and towels.

Please check the specific property listing for detailed amenities."""
    },
    {
        "question": "Are pets allowed at the properties?",
        "answer": """Pet policies differ by property. Some of our properties are pet-friendly, while others are not. Please refer to the property's listing for its pet policy."""
    },
    {
        "question": "What is the minimum stay requirement?",
        "answer": """Minimum stay requirements vary depending on the property and the season. Generally, the minimum stay ranges from 2 to 3 nights. Please check the property's listing for exact details."""
    },
    {
        "question": "What are the check-in and check-out times?",
        "answer": """Check-in and check-out times vary by property. Detailed information will be provided upon booking confirmation."""
    },
    {
        "question": "Is Wi-Fi available at the properties?",
        "answer": """Yes, most of our properties offer complimentary Wi-Fi. Wi-Fi details will be provided upon arrival."""
    },
    {
        "question": "What is the cancellation policy?",
        "answer": """Cancellation policies vary by property and may include Firm, Flexible, or Moderate options. Please review the cancellation policy on the property's listing before booking."""
    },
    {
        "question": "Are cleaning services provided during my stay?",
        "answer": """Cleaning services depend on the property. Some properties offer weekly cleaning, while others provide services upon request or at an additional fee. Please refer to the property's listing for details."""
    },
    {
        "question": "Do you provide any additional amenities like toiletries or welcome packs?",
        "answer": """Many of our properties provide basic toiletries such as body wash, as well as complimentary coffee and tea. Some properties may also offer welcome packs including milk, bottled water, biscuits, or rusks. Details can be found in the property's listing."""
    },
    {
        "question": "Is parking available at the properties?",
        "answer": """Yes, most of our properties offer free parking facilities. Please check the property's listing for parking details."""
    },
    {
        "question": "How many people can stay at each property?",
        "answer": """Each property has a maximum occupancy limit, which varies depending on its size:

- **Clifftop Cabin**: Sleeps 2 guests.
- **Wildside Cabin**: Sleeps 2 guests.
- **Rondebos Retreat**: Sleeps 7 guests.
- **Hill Penthouse Plett**: Sleeps 6 guests.
- **Hill Sea-View Apartment**: Sleeps 6 guests.
- **Arrowood Apartment**: Sleeps 4 guests.
- **Toplis Vista**: Sleeps 12 guests.
- **Keurbooms River Apartment**: Sleeps 6 guests.
- **Dassen Eiland Home**: Sleeps 6 guests.
- **Panorama Seaview Flat**: Sleeps 4 guests."""
    },
    {
        "question": "What are the bed configurations in the properties?",
        "answer": """Bed configurations vary by property. For example:

- **Clifftop Cabin**: 1 Queen bed.
- **Wildside Cabin**: 1 Queen bed.
- **Rondebos Retreat**: Combination of King, Queen, and Single beds.
- **Hill Penthouse Plett**: 1 Queen, 1 Double, 2 Singles.
- **Hill Sea-View Apartment**: 1 King XL, 4 Singles.
- **Arrowood Apartment**: 4 Single beds.
- **Toplis Vista**: Mix of King, Queen, and Single beds across 6 bedrooms.
- **Keurbooms River Apartment**: 3 Double beds.
- **Dassen Eiland Home**: 1 King XL, 1 Queen, 2 Singles.
- **Panorama Seaview Flat**: 1 King, 2 Singles."""
    },
    {
        "question": "Are there any additional fees or deposits required?",
        "answer": """Some properties may require a refundable breakage deposit or have additional fees for cleaning services. Details will be provided during the booking process."""
    },
    {
        "question": "What are the payment options?",
        "answer": """Payment options include major credit cards and bank transfers. Secure payment methods are available through the booking platforms."""
    },
    {
        "question": "Can I modify my booking after it has been confirmed?",
        "answer": """Modification policies vary by property. Please contact us directly to discuss any changes to your booking."""
    },
    {
        "question": "Are there any house rules I should be aware of?",
        "answer": """Yes, each property has its own set of house rules, which may include policies on smoking, noise levels, and pets. These will be provided upon booking and are also available in the property's listing."""
    },
    {
        "question": "What should I do if I have an issue during my stay?",
        "answer": """We are committed to ensuring you have a pleasant stay. If you encounter any issues, please contact our customer service team immediately for assistance."""
    },
    {
        "question": "Do the properties have safety features like fire extinguishers and first aid kits?",
        "answer": """Yes, most properties are equipped with safety features such as fire extinguishers and first aid kits. Please check the property's listing for specific safety amenities."""
    },
    {
        "question": "How far in advance should I book?",
        "answer": """We recommend booking as early as possible to secure your preferred dates, especially during peak seasons. Some properties have advance notice requirements ranging from 1 to 15 days."""
    },
    {
        "question": "What are the check-in procedures?",
        "answer": """Check-in procedures vary by property. Some properties offer self-check-in with lockboxes, while others may have a meet-and-greet service. Detailed instructions will be provided upon booking confirmation."""
    },
    {
        "question": "Is linen and towels provided?",
        "answer": """Yes, all our properties provide fresh linen and towels for your stay."""
    },
    {
        "question": "Are there any special COVID-19 measures in place?",
        "answer": """We adhere to all recommended health and safety guidelines to ensure our properties are clean and safe. Enhanced cleaning protocols are in place."""
    },
    {
        "question": "Is there support for guests with disabilities?",
        "answer": """Some properties may be more accessible than others. Please contact us to discuss any specific accessibility needs you may have."""
    },
    {
        "question": "How can I get directions to the property?",
        "answer": """Detailed directions will be provided upon booking confirmation, along with the property's address and any access codes if applicable."""
    },
    {
        "question": "Are group bookings allowed?",
        "answer": """Yes, properties like **Toplis Vista** and **Rondebos Retreat** are ideal for group bookings. Please ensure the group's size does not exceed the property's maximum occupancy."""
    },
    {
        "question": "Is there a minimum age requirement for booking?",
        "answer": """Guests must be at least 18 years old to book a property. Some properties may have additional age restrictions, which will be noted in the listing."""
    },
    {
        "question": "Do you offer any long-term rental options?",
        "answer": """Some properties may offer discounts for long-term stays. Please contact us to discuss availability and rates."""
    },
    {
        "question": "Are events or parties allowed at the properties?",
        "answer": """Our properties are intended for accommodation purposes only. Events or parties are not permitted unless explicitly agreed upon prior to booking."""
    },
    {
        "question": "Can I check-in early or check-out late?",
        "answer": """Early check-in or late check-out may be possible, subject to availability and prior arrangement. Additional fees may apply."""
    },
    {
        "question": "What is the maximum stay duration?",
        "answer": """Maximum stay durations vary by property, ranging from 15 to 30 days. Please refer to the property's listing for exact details."""
    },
    {
        "question": "What is the advance notice required for booking?",
        "answer": """Advance notice requirements vary from 1 day to up to 15 days, depending on the property. Please check the property's listing for specific requirements."""
    }
]

def find_answer(user_question):
    # Normalize the user question
    user_question = user_question.lower().strip()

    # Try to find a direct match
    for faq in faqs:
        if user_question == faq['question'].lower():
            return faq['answer']

    # Keyword matching
    keywords = {
        "properties": "What properties are available for rental?",
        "book": "How can I book a property?",
        "amenities": "What amenities are available at the properties?",
        "pets": "Are pets allowed at the properties?",
        "minimum stay": "What is the minimum stay requirement?",
        "check-in": "What are the check-in and check-out times?",
        "wifi": "Is Wi-Fi available at the properties?",
        "cancellation": "What is the cancellation policy?",
        "cleaning": "Are cleaning services provided during my stay?",
        "welcome pack": "Do you provide any additional amenities like toiletries or welcome packs?",
        "parking": "Is parking available at the properties?",
        "occupancy": "How many people can stay at each property?",
        "bed": "What are the bed configurations in the properties?",
        "fees": "Are there any additional fees or deposits required?",
        "payment": "What are the payment options?",
        "modify": "Can I modify my booking after it has been confirmed?",
        "house rules": "Are there any house rules I should be aware of?",
        "issue": "What should I do if I have an issue during my stay?",
        "safety": "Do the properties have safety features like fire extinguishers and first aid kits?",
        "advance booking": "How far in advance should I book?",
        "directions": "How can I get directions to the property?",
        "group bookings": "Are group bookings allowed?",
        "age requirement": "Is there a minimum age requirement for booking?",
        "long-term": "Do you offer any long-term rental options?",
        "events": "Are events or parties allowed at the properties?",
        "early check-in": "Can I check-in early or check-out late?",
        "linen": "Is linen and towels provided?",
        "covid": "Are there any special COVID-19 measures in place?",
        "disabilities": "Is there support for guests with disabilities?",
        "maximum stay": "What is the maximum stay duration?",
        "advance notice": "What is the advance notice required for booking?"
    }

    for keyword, question in keywords.items():
        if keyword in user_question:
            # Find the corresponding answer
            for faq in faqs:
                if faq['question'] == question:
                    return faq['answer']

    return "I'm sorry, I couldn't find an answer to your question. Please contact our customer support for assistance."

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'answer': "Invalid request. Please provide a question."}), 400

    user_question = data['question']
    answer = find_answer(user_question)

    # Convert the answer from Markdown to HTML
    answer_html = markdown.markdown(answer)

    return jsonify({'answer': answer_html})

if __name__ == "__main__":
    app.run(debug=True)