import axios from 'axios';
import { ADD_ACCOUNT, CHANGE_INFO_ACCOUNT, DELETE_ACCOUNT, GET_ACCOUNTS } from '../actions/types';

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

// Get accounts

export const getAccounts = () => dispatch => {
    axios.get('api/account/')
        .then(result => {
            dispatch({
                type: GET_ACCOUNTS,
                payload: result.data
            });
        }).catch(error => console.log(error));
};