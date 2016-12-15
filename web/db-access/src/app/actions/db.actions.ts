import { Injectable } from '@angular/core';
import { Action, createAction } from 'redux-actions';

@Injectable()
export class DbActions {
    public static ADD_DBS: string = '[dbReducer] Add Dbs';
    public static ADD_TABLES: string = '[dbReducer] Add Tables';
    public static ADD_FIELDS: string = '[dbReducer] Add Fields';
    public static ADD_ROWS: string = '[dbReducer] Add Rows';
    public static SET_CONN: string = '[dbReducer] Set Connection';

    public addDbs: (dbs: any) => Action<any> = createAction(DbActions.ADD_DBS);
    public addTables: (tables: any) => Action<any> = createAction(DbActions.ADD_TABLES);
    public addRows: (rows: any) => Action<any> = createAction(DbActions.ADD_ROWS);
    public addFields: (fields: any) => Action<any> = createAction(DbActions.ADD_FIELDS);
    public setDbConn: (dbConn: any) => Action<any> = createAction(DbActions.SET_CONN);
}
