import { Injectable } from "@angular/core";
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { DbProxy } from './db.proxy';
import { DbConnModel } from './db.models';
import { Observable } from "rxjs/Rx";

@Injectable()
export class DbRepository {

    constructor(private http: Http) {}

    private dbConnToQueryString(dbConn: DbConnModel): string {
        return `host=${dbConn.ip}&port=${dbConn.port}&user=${dbConn.user}&password=${dbConn.password}`;
    }

    public getDbs(dbConnModel: DbConnModel): Observable<Response> {
        let query: string =
            `host=${dbConnModel.ip}&port=${dbConnModel.port}&user=${dbConnModel.user}&password=${dbConnModel.password}`;
        return this.http.get(`${dbConnModel.url}dbs?${query}`, new RequestOptions({
            headers: new Headers({
                'Content-Type': 'application/json',
            })
        }));
    }
}
