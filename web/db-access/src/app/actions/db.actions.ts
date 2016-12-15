import { Injectable } from '@angular/core';
import { Action, createAction } from 'redux-actions';

@Injectable()
export class DbActions {
    public static GET_DBS: string = '[app] Get Dbs';
    public static GET_TABLES: string = '[app] Get Tables';
    public static GET_FIELDS: string = '[app] Get Fields';
    public static GET_ROWS: string = '[app] Get Rows';
    public static SET_CONN: string = '[app] Set Connection';

    public getDbs: (dbs: any) => Action<any> = createAction(DbActions.GET_DBS);
    public getTables: (tables: any) => Action<any> = createAction(DbActions.GET_TABLES);
    public getRows: (rows: any) => Action<any> = createAction(DbActions.GET_ROWS);
    public getFields: (fields: any) => Action<any> = createAction(DbActions.GET_FIELDS);
    public setDbConn: (dbConn: any) => Action<any> = createAction(DbActions.SET_CONN);
}
