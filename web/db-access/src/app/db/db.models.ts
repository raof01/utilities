export interface DbConnModel {
    url: string;
    ip: string;
    port: string;
    user: string;
    password: string;
}

export interface DbState {
    dbConn: DbConnModel;
    dbs: string[];
    tables: string[];
    fields: string[];
    rows: any[];
}
