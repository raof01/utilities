import { ConnActions } from '../actions/conn.action';
import { Action, handleActions } from 'redux-actions';

import { DbConnModel } from '../db/db.models';

export const ConnReducer: (state: DbConnModel, action: Action<DbConnModel>) => DbConnModel = handleActions(
    <any>{
        [ConnActions.SET_CONN]: setDbConn
    },
    {
        url: '',
        ip: '',
        port: '',
        user: '',
        password: ''
    }
);

function setDbConn(state: DbConnModel, action: Action<DbConnModel>): DbConnModel {
    // TODO
    return action.payload;
}
