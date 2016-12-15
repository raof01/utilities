import { DbActions } from '../actions/db.actions';
import { Action, handleActions } from 'redux-actions';

import { DbState, DbConnModel } from '../db/db.models';

export const DbReducer: (state: DbState, action: Action<any>) => DbState = handleActions(
    <any>{
        [DbActions.ADD_DBS]: addDbs,
        [DbActions.ADD_TABLES]: addTables,
        [DbActions.ADD_FIELDS]: addFields,
        [DbActions.ADD_ROWS]: addRows,
        [DbActions.SET_CONN]: setDbConn
    },
    {
        dbConn: undefined,
        dbs: undefined,
        tables: undefined,
        fields: undefined,
        rows: undefined,
    }
);

function addDbs(state: DbState, action: Action<string[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: action.payload,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function addTables(state: DbState, action: Action<string[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function addFields(state: DbState, action: Action<string[]>): DbState {
    // TODO
    return {
        dbConn: state.dbConn,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}

function addRows(state: DbState, action: Action<any[]>): DbState {
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
        dbConn: action.payload,
        dbs: state.dbs,
        tables: state.tables,
        fields: state.fields,
        rows: state.rows
    }
}
