odoo.define('cardknox_payment_pos.payment', function(require) {
    'use strict';

    const PaymentInterface = require('point_of_sale.PaymentInterface');
    const { Gui } = require('point_of_sale.Gui');
    const { _t } = require('web.core');
    const Registries = require('point_of_sale.Registries');

    class CardknoxPaymentTerminal extends PaymentInterface {
        
        constructor(pos, payment_method) {
            super(pos, payment_method);
            this.payment_method = payment_method;
        }

        async send_payment_request(cid) {
            this.set_payment_status('waiting');
            const order = this.pos.get_order();
            const paymentline = order.get_paymentline(cid);
           

           

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
                    Gui.showPopup('ErrorPopup', {
                        title: _t('Payment Failed'),
                        body: transactionData.error || _t('The payment was declined by the terminal.'),
                    });
                    paymentline.set_payment_status('retry');
                    return false;
                }
            } catch (error) {
                Gui.showPopup('ErrorPopup', {
                    title: _t('Connection Error'),
                    body: _t('Could not connect to the local CardKnox server. Error: ') + error.message,
                });
                paymentline.set_payment_status('retry');
                return false;
            }
        }
    }

    Registries.PaymentMethods.add('cardknox', CardknoxPaymentTerminal);

    return CardknoxPaymentTerminal;
});
