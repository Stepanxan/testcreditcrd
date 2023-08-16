import xlsxwriter
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import deal, payment_schedule, payment
import json


connection_str = 'mysql+pymysql://root:19982804@localhost/task1'
engine = create_engine(connection_str)


Session = sessionmaker(bind=engine)
session = Session()
overdue_clients_count_query = (
    session.query(func.count(payment.payment_date))
    .join(payment_schedule, payment.payment_id == payment_schedule.payment_schedule_id)
    .filter(payment.payment_date < payment_schedule.schedule_date)
    .scalar()
)

#print(f"Number of overdue clients: {overdue_clients_count_query}")
result = {"Кількість клієнтів що прострочили платіж": overdue_clients_count_query}
with open("result.json", "w") as json_file:
    json.dump(result, json_file)
print("Результат збережено до 'result.json'")

# Підрахунок % суми оплати клієнтів відносно суми необхідної за плановими платежами
payment_vs_schedule_percentage_query = (
    session.query(
        deal.deal_id,
        deal.deal_number,
        ((func.sum(deal.loan_amount) - func.sum(payment_schedule.schedule_amount)) / func.sum(deal.loan_amount)) * 100.0
    )
    .join(payment_schedule, deal.deal_id == payment_schedule.deal_id)
    .group_by(deal.deal_id)
    .all()
)
session.close()



workbook = xlsxwriter.Workbook('Результат.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(0, 0, 10)
worksheet.set_column(1, 1, 10)
worksheet.set_column(2, 2, 70)

bold_format = workbook.add_format({'bold': True})
worksheet.write(0, 0, 'Deal Number', bold_format)
worksheet.write(0, 1, 'Deal ID', bold_format)
worksheet.write(0, 2, '% оплачено клієнтом відносно всієї суми за плановими платежами', bold_format)



percent_format = workbook.add_format({'num_format': '0.00%'})

row = 1
for deal_id, deal_number, payment_percentage in payment_vs_schedule_percentage_query:
    worksheet.write(row, 0, deal_number)
    worksheet.write(row, 1, deal_id)
    worksheet.write(row, 2, payment_percentage / 100, percent_format)
    row += 1

workbook.close()

print("Дані збережено в Результат.xlsx")
