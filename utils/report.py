from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_report(
    filename,
    income,
    expenses,
    savings,
    score
):

    doc = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()


    content = []


    content.append(
        Paragraph(
            "Personal Finance Report",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    text = f"""

    Total Income: ₹{income:,.0f}

    Total Expenses: ₹{expenses:,.0f}

    Savings: ₹{savings:,.0f}

    Financial Health Score:
    {score}/100

    """


    content.append(
        Paragraph(
            text,
            styles["BodyText"]
        )
    )


    doc.build(content)