/** @odoo-module **/

import { _t } from '@web/core/l10n/translation';
import { loadJS } from '@web/core/assets';

import paymentForm from '@payment/js/payment_form';
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
paymentForm.include({
    events: Object.assign({}, paymentForm.prototype.events, {
        'submit': '_onSubmit',
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
        const cardknoxForm = this.el.querySelector('[data-provider-code="cardknox"]');
        if (!cardknoxForm) {
            return;
        }

        // Load the Cardknox iFields JavaScript library
        loadJS('https://cdn.cardknox.com/ifields/2.15.2302.0801/ifields.min.js')
            .then(() => {
                if (window.setAccount) {

                    let cardknoxInlineForm = document.querySelector('[name="cardknox_element_container"]')
                    let cardknoxInlineFormValues = JSON.parse(cardknoxInlineForm.dataset['cardknoxInlineValues'])
                    this.cardknoxInlineFormValues = cardknoxInlineFormValues
                 
                    
                    const ifieldsToken = cardknoxInlineFormValues.ifields_token;
                    
                    if (!ifieldsToken) {
                        console.error('Cardknox iFields token is missing');
                        return;
                    }

                    // Initialize iFields
                    setAccount(ifieldsToken, "Odoo Cardknox Integration","1.0");
                    
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
                    window.addIfieldCallback('input', function(data) {
                        // data.ifieldName here will be 'card-number', 'exp-date', or 'cvv'
                        const errorElement = document.querySelector(`[data-ifields-id="${data.ifieldName}-error"]`);
                        if (errorElement) {
                            if (data.status) {
                                errorElement.textContent = '';
                            } else {
                                errorElement.textContent = data.errorMessage;
                            }
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Failed to load Cardknox iFields library:', error);
            });
    },

    /**
     * Handle form submission for Cardknox payments.
     *
     * @private
     * @param {Event} ev - The submit event
     * @return {void}
     */
    _onSubmit(ev) {
        if (this.getPaymentProviderCode() !== 'cardknox') {
            return;
        }
        
        ev.preventDefault();
        ev.stopPropagation();
        
        // Get the form data
        const form = ev.currentTarget;
        const data = new FormData(form);
        const actionUrl = form.getAttribute('action');
        
        // Show loading state
        this._setLoading(true);
        
        // Get tokenized card data from iFields
        window.getTokens(
            (tokens) => {
                // Check if tokenization was successful
                 console.log(11111111111111111111111111111111111111111111111111111111111111)
                 
                if (tokens.cardToken) {
                    // Add the token to the form data
                   
                    data.append('cardknox_token', tokens.cardToken);
                    data.append("card_num",)
                    data.append("cvv",)
                    
                    // Submit the form with the token
                    this._submitForm(actionUrl, data);
                } else {
                    // Handle tokenization error
                    this._displayError(
                        _t("Payment Processing Error"),
                        _t("Failed to tokenize card information. Please check your card details and try again.")
                    );
                    this._setLoading(false);
                }
            },
            (errors) => {
                // Handle tokenization error
                this._displayError(
                    _t("Payment Processing Error"),
                    _t("Failed to tokenize card information. Please check your card details and try again.")
                );
                console.error('Cardknox tokenization errors:', errors);
                this._setLoading(false);
            }
        );
    },

    /**
     * Submit the form with tokenized data.
     *
     * @private
     * @param {string} url - The form action URL
     * @param {FormData} formData - The form data including the token
     * @return {void}
     */
    _submitForm(url, formData) {
        // Convert FormData to URL-encoded string
        const data = Array.from(formData.entries())
            .map(x => `${encodeURIComponent(x[0])}=${encodeURIComponent(x[1])}`)
            .join('&');
        
        // Create and submit a hidden form
        const hiddenForm = document.createElement('form');
        hiddenForm.setAttribute('method', 'post');
        hiddenForm.setAttribute('action', url);
        hiddenForm.setAttribute('style', 'display: none;');
        
        const input = document.createElement('input');
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', 'payment_data');
        input.setAttribute('value', data);
        
        hiddenForm.appendChild(input);
        document.body.appendChild(hiddenForm);
        
        hiddenForm.submit();
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
    async _processRedirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'cardknox') {
            return this._super(...arguments);
        }
        
        // For Cardknox, we handle the payment in the _onSubmit method
        // This method is called when the form is submitted via the "Pay Now" button
        return Promise.resolve();
    }
});
