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
}
