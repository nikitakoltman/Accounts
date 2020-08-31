import React, { Component, Fragment } from 'react';
import Modals from './Modals';
import Table from './Table';

export class Account extends Component {
    render() {
        return (
            <Fragment>
                <Table/>
                <Modals/>
            </Fragment>
        )
    }
}

export default Account
