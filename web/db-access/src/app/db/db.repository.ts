import { Injectable } from "@angular/core";
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { Proxy } from './db/db.proxy';
import { DbConnModel } from './db.models';
import { Observable } from "rxjs/Rx";

@Injectable()
export class DbRepository {

    constructor(private http: Http) {}
}
