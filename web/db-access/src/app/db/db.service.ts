import { Injectable } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { Proxy } from '../proxy.service';
import { DbConnModel } from './db-conn.model';

@Injectable()
export class DbService {

    constructor(private http: Http, private proxyService: Proxy) {
    }

    public getDbs(dbConnModel: DbConnModel) : void {
        /*let body: string = `{
            host: ${ip},
            port: ${port},
            user: ${user},
            password: ${password}
        }`;*/
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}`;
        this.http.get(`${dbConnModel.url}dbs?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyDbs(value.json());
        });
    }

    public getTables(dbConnModel: DbConnModel, dbName: string) {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}&dbName=${dbName}`;
        this.http.get(`${dbConnModel.url}tables?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyTables(value.json());
        });
    }

    public getColumns(dbConnModel: DbConnModel, dbName: string, tblName: string) {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}&dbName=${dbName}&tableName=${tblName}`;
        this.http.get(`${dbConnModel.url}columns?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            this.proxyService.notifyFields(value.json());
        });
    }

    public getValues(dbConnModel: DbConnModel, dbName: string, tblName: string, fields: string[]) {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}&dbName=${dbName}&tableName=${tblName}&fields=${fields.join(',')}`;
        this.http.get(`${dbConnModel.url}table?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        })).subscribe((value: Response) => {
            // TODO: send notification to a table component
            this.proxyService.notifyRows(value.json());
        });
    }
}