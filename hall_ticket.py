from fpdf import FPDF


def generate_hall_ticket(email, subjects):
    pdf = FPDF()
    pdf.add_page()
    pdf.image('static\\images\\images.jpg', x=47, y=30)
    pdf.set_font('arial', 'B', 23.0)
    pdf.cell(ln=0, h=7.0, align='C', w=0, txt="Hall Ticket", border=0)
    pdf.rect(20, 20, 165, 250)

    x = 30
    y = 90
    for subject in subjects:
        pdf.set_font('arial', 'B', 13.0)
        pdf.set_xy(x, y)
        y += 6
        pdf.cell(ln=0, h=7.0, align='L', w=0, txt='{}({})'.format(subject.subject_name, subject.subject_code), border=0)
        pdf.set_font('arial', 'B', 8.0)
        pdf.set_xy(x, y)
        y += 6
        pdf.cell(ln=0, h=7.0, align='L', w=0, txt=subject.exam_date, border=0)

    new = ""
    for i in email:
        if i == '.':
            new += '_'
        else:
            new += i

    pdf.output('static\\pdf\\{}.pdf'.format(new), 'F')
    return 'static\\pdf\\{}.pdf'.format(new)


if __name__ == '__main__':
    pass
