import { DbAccessPage } from './app.po';

describe('db-access App', function() {
  let page: DbAccessPage;

  beforeEach(() => {
    page = new DbAccessPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
