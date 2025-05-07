/** @odoo-module **/
/* global Accept */

import { _t } from '@web/core/l10n/translation';
import { loadJS } from '@web/core/assets';

import paymentForm from '@payment/js/payment_form';
import { rpc, RPCError } from '@web/core/network/rpc';

paymentForm.include({

        // #=== DOM MANIPULATION ===#

    /**
     * Prepare the inline form of Authorize.net for direct payment.
     *
     * @private
     * @param {number} providerId - The id of the selected payment option's provider.
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The online payment flow of the selected payment option.
     * @return {void}
     */
    async _processRedirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues){
        if(providerCode!= 'cardknox'){
            await this._super(...arguments);
            return;
        }

        
    }

})