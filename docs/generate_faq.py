import json


def fill_faq(faq_json_path: str, faq_rst_path: str) -> None:
    """
    Function to fill the FAQ .rst file with questions and answers from a JSON file.

    Args:
        faq_json_path (str): The path of the JSON file containing the FAQs
        faq_rst_path (str): The path of the .rst file to be filled
    """

    # Load the FAQs from the JSON file
    with open(faq_json_path, "r") as faq_file:
        faqs = json.load(faq_file)

    # Create/open the FAQ .rst file
    with open(faq_rst_path, "w") as faq_rst_file:
        # Write the title of the FAQ
        faq_rst_file.write("Frequently Asked Questions\n")
        faq_rst_file.write("==========================\n\n")

        # Write each question and answer
        for i, faq in enumerate(faqs, start=1):
            question = faq["question"]
            answer = faq["answer"].replace("\\n", "\n   ")

            faq_rst_file.write(f".. dropdown:: Q: {question}\n")
            faq_rst_file.write("   :container: + shadow\n")
            faq_rst_file.write("   :title: bg-primary text-white text-center\n")
            faq_rst_file.write("   :body: bg-dark font-weight-light \n\n")
            faq_rst_file.write(f"   A: {answer}\n\n")


if __name__ == "__main__":
    fill_faq("faq.json", "faq.rst")
