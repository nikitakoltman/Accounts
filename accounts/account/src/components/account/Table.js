import React, { Component, Fragment} from 'react';
import { connect } from 'react-redux';
import { PropTypes } from 'prop-types';
import { getAccounts } from '../../actions/accounts'

class Table extends Component {

    static propTypes = {
        accounts: PropTypes.array.isRequired
    };

    componentDidMount() {
        this.props.getAccounts();
    }

    render() {
        return (
            <Fragment>
                <div>
                    table
                </div>
            </Fragment>
        )
    }
}

const mapStateToProps = (state) => ({
    accounts: state.accounts.accounts
});

export default connect(mapStateToProps, { getAccounts })(Table);
