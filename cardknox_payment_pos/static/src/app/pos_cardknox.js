import { _t } from "@web/core/l10n/translation";
import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { register_payment_method } from "@point_of_sale/app/store/pos_store";

    class CardknoxPaymentTerminal extends PaymentInterface {
        
        constructor(pos, payment_method) {
            super(pos, payment_method);
            this.payment_method = payment_method;
        }

        async send_payment_request(cid) {
            await super.send_payment_request(...arguments);
        
            
            const order = this.pos.get_order();
            const paymentline = order.get_selected_paymentline();
            paymentline.set_payment_status('waiting');
           

           

            try {
                const url = new URL("https://localemv.com:8887/");
                url.searchParams.append('xCommand', 'cc:sale');
                url.searchParams.append('xInvoice', order.get_name());
                url.searchParams.append('xAmount', paymentline.get_amount());

                const response = await fetch(url, {
                    method: 'GET',
                });

                if (!response.ok) {
                    const errorBody = await response.text();
                    throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
                }

                const transactionData = await response.json();

                if (transactionData.success) {
                    // If the local server confirms the payment, we set the details
                    // on the payment line and mark it as done.
                    paymentline.transaction_id = transactionData.xRefNum;
                    paymentline.card_type = transactionData.xCardType;
                    paymentline.cardholder_name = transactionData.xMaskedCardNumber;
                    paymentline.set_payment_status('done');
                    return true;
                } else {
                   this.showError( _t('Payment Failed'),transactionData.error || _t('The payment was declined by the terminal.'));
                   
                    paymentline.set_payment_status('retry');
                    return false;
                }
            } catch (error) {
                this.showError(_t('Connection Error'), _t('Could not connect to the local CardKnox server. Error: ') + error.message);
                paymentline.set_payment_status('retry');
                return false;
            }
        }

        showError(title, message) {
            this.env.services.dialog.add(AlertDialog, {
            title: title,
            body: message,
        });
        }
    }

register_payment_method('cardknox', CardknoxPaymentTerminal);