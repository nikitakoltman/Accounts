import { ADD_ACCOUNT, CHANGE_INFO_ACCOUNT, DELETE_ACCOUNT, GET_ACCOUNTS } from '../actions/types';

const initialState = {
    accounts: []
};

export default function (state = initialState, action) {
    switch (action.type) {
        case ADD_ACCOUNT:
            return {
                ...state,
                accounts: action.payload
            };
        default:
            return state;
    }
};