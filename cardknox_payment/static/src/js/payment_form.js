/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";

import paymentForm from "@payment/js/payment_form";
import { rpc, RPCError } from '@web/core/network/rpc';
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
paymentForm.include({
  events: Object.assign({}, paymentForm.prototype.events, {
    submit: "_onSubmit",
  }),

  /**
   * @override
   */
  async start() {
    await this._super(...arguments);
    this._cardknoxSetupForm();
  },

  /**
   * Setup the Cardknox iFields form when the payment option is selected.
   *
   * @private
   * @return {void}
   */
  _cardknoxSetupForm() {
    const cardknoxForm = this.el.querySelector(
      '[data-provider-code="cardknox"]'
    );
    if (!cardknoxForm) {
      return;
    }

    // Load the Cardknox iFields JavaScript library
    loadJS("https://cdn.cardknox.com/ifields/2.15.2302.0801/ifields.min.js")
      .then(() => {
        if (window.setAccount) {
          let cardknoxInlineForm = document.querySelector(
            '[name="cardknox_element_container"]'
          );
          let cardknoxInlineFormValues = JSON.parse(
            cardknoxInlineForm.dataset["cardknoxInlineValues"]
          );
          this.cardknoxInlineFormValues = cardknoxInlineFormValues;

          const ifieldsToken = cardknoxInlineFormValues.ifields_token;

          if (!ifieldsToken) {
            console.error("Cardknox iFields token is missing");
            return;
          }

          // Initialize iFields
          setAccount(ifieldsToken, "Odoo Cardknox Integration", "1.0");

          // The following styling and auto-formatting calls might be handled by the iframe's data-attributes
          // or might still be applicable. For now, we assume the iframe method is more self-contained.
          // If specific styling or formatting is needed beyond what the iframe defaults provide,
          // these or similar API calls might be re-enabled or adapted.

          // window.setIfieldStyle('card-number', 'height:34px;width:100%;border:1px solid #ccc;border-radius:4px;padding:6px 12px;');
          // window.enableAutoFormatting(); // This might be controlled by Cardknox default for iframes or a data-attribute

          // window.setIfieldStyle('exp-date', 'height:34px;width:100%;border:1px solid #ccc;border-radius:4px;padding:6px 12px;');

          // window.setIfieldStyle('cvv', 'height:34px;width:100%;border:1px solid #ccc;border-radius:4px;padding:6px 12px;');

          // Add event listeners for field validation
          // This callback targets elements by id like `card-number-error`.
          // We've kept `data-ifields-id` on the error divs in the template,
          // assuming the iFields library might use these for error messages.
          window.addIfieldCallback("input", function (data) {
            // data.ifieldName here will be 'card-number', 'exp-date', or 'cvv'
            const errorElement = document.querySelector(
              `[data-ifields-id="${data.ifieldName}-error"]`
            );
            if (errorElement) {
              if (data.status) {
                errorElement.textContent = "";
              } else {
                errorElement.textContent = data.errorMessage;
              }
            }
          });
        }
      })
      .catch((error) => {
        console.error("Failed to load Cardknox iFields library:", error);
      });
  },

  /**
   * Process the redirect flow for Cardknox payments.
   *
   * @override
   * @private
   * @param {string} providerCode - The code of the selected payment option's provider
   * @param {number} paymentOptionId - The id of the selected payment option
   * @param {string} paymentMethodCode - The code of the selected payment method, if any
   * @param {Object} processingValues - The processing values of the transaction
   * @return {Promise} - Resolves when the payment has been processed
   */
  async _processRedirectFlow(
    providerCode,
    paymentOptionId,
    paymentMethodCode,
    processingValues
  ) {
    if (providerCode !== "cardknox") {
      return this._super(...arguments);
    }
    getTokens(
      (s) => {
        console.log(processingValues);
        console.log(
          1,
          document.querySelector('input[name="xCardNum"]'),
          2,
          document.querySelector('input[name="xCVV"]')
        );
        let paymentInfo ={
            cardNo:document.querySelector("#xcard_num").value,
            exp:document.querySelector("#exp").value,
            cvv:document.querySelector("#xcvv").value
        }

        rpc('/payment/cardknox/payment',{
            payment_info:paymentInfo,
            payment_perems:processingValues
        }).then(()=>{
             window.location = '/payment/status';
        }).catch((error)=>{
            if (error instanceof RPCError) {
                this._displayErrorDialog(_t("Payment processing failed"), error.data.message);
                this._enableButton();
            } else {
                return Promise.reject(error);
            }
        })
      },
      (e) => {},
      3000
    );
  },
});
