import { DbActions } from '../actions/db.actions';
import { Action, handleActions } from 'redux-actions';

import { DbState, DbConnModel } from '../db/db.models';

export const DbReducer: (state: DbState, action: Action<any>) => DbState = handleActions(
    <any>{
        [DbActions.GET_DBS]: getDbs,
        [DbActions.GET_TABLES]: getTables,
        [DbActions.GET_FIELDS]: getFields,
        [DbActions.GET_ROWS]: getRows,
        [DbActions.SET_CONN]: setDbConn,
    },
    {
        dbConn: undefined,
        dbs: undefined,
        tables: undefined,
        fields: undefined,
        rows: undefined,
    }
);

function getDbs(state: DbState, action: Action<string[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function getTables(state: DbState, action: Action<string[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function getFields(state: DbState, action: Action<string[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function getRows(state: DbState, action: Action<any[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function setDbConn(state: DbState, action: Action<DbConnModel>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}
