from intuitquickbooks.objects.creditmemo import CreditMemo
from intuitquickbooks.objects.customer import Customer
from intuitquickbooks.objects.detailline import SalesItemLine
from intuitquickbooks.objects.detailline import SalesItemLineDetail
from intuitquickbooks.objects.item import Item
from tests.integration.test_base import QuickbooksTestCase


class CreditMemoTest(QuickbooksTestCase):
    def test_create(self):
        customer = Customer.all(max_results=1, qb=self.qb_client)[0]
        item = Item.all(max_results=1, qb=self.qb_client)[0]

        credit_memo = CreditMemo()
        credit_memo.CustomerRef = customer.to_ref()

        detail_line = SalesItemLine()
        detail_line.LineNum = 1
        detail_line.Description = "Test Description"
        detail_line.Amount = 100
        detail_line.DetailType = "SalesItemLineDetail"
        detail_line.SalesItemLineDetail = SalesItemLineDetail()
        detail_line.SalesItemLineDetail.ItemRef = item.to_ref()
        credit_memo.Line.append(detail_line)
        credit_memo.save(qb=self.qb_client)

        query_credit_memo = CreditMemo.get(credit_memo.Id, qb=self.qb_client)

        self.assertEquals(credit_memo.Id, query_credit_memo.Id)
        self.assertEquals(query_credit_memo.CustomerRef.value, customer.Id)

        line = query_credit_memo.Line[0]
        self.assertEquals(line.LineNum, 1)
        self.assertEquals(line.Description, "Test Description")
        self.assertEquals(line.Amount, 100)
        self.assertEquals(line.DetailType, "SalesItemLineDetail")
        self.assertEquals(line.SalesItemLineDetail.ItemRef.value, item.Id)

    def test_update(self):
        credit_memo = CreditMemo.all(max_results=1, qb=self.qb_client)[0]
        credit_memo.PrivateNote = "Test"
        credit_memo.save(qb=self.qb_client)

        query_credit_memo = CreditMemo.get(credit_memo.Id, qb=self.qb_client)
        self.assertEquals(query_credit_memo.PrivateNote, "Test")


