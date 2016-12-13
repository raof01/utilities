import { Injectable, Component } from '@angular/core';
import { Http, Request, Response, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { DbService } from './db.service';
import { Proxy } from '../proxy.service';
import { DbsComponent } from './dbs.component';
import { DbConnModel } from './db-conn.model';

@Component({
    selector: 'db-login',
    templateUrl: './db-login.component.html',
    styleUrls: ['../app.component.css']
})

/*
 * NOTE:
 * TODO: db-access logic should be in server side, instead of client side
 */
@Injectable()
export class DbLoginComponent {
    title: string = 'Login';
    private dbConnModel: DbConnModel = {url: 'http://localhost:3000/', ip: '', port: '', user: '', password: ''};
    private url: string = undefined;
    private selectedDb: string = undefined;
    private selectedTable: string = undefined;
    private fields: string[] = undefined;

    constructor(
        private dbService: DbService,
        private proxyService: Proxy
    ) {
        this.proxyService.subscribeDbSelected(this.onDbSelected.bind(this));
        this.proxyService.subscribeTableSelected(this.onTableSelected.bind(this));
        this.proxyService.subscribeFields(this.onColumnsGot.bind(this));
    }

    private onColumnsGot(v: string[]) {
        this.fields = v;
        this.dbService.getValues(this.dbConnModel, this.selectedDb, this.selectedTable, this.fields);
    }

    private onDbSelected(v: string) {
        this.selectedDb = v;
        this.dbService.getTables(this.dbConnModel, v);
    }

    private onTableSelected(v: string) {
        this.selectedTable = v;
        this.dbService.getColumns(this.dbConnModel, this.selectedDb, v);
    }

    public onClick(event) {
        this.dbService.getDbs(this.dbConnModel);
    }
}
