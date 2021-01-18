import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewInit {

  @ViewChild('repliesList') repliesList;
  @ViewChild('repliesDiv') repliesDiv;

  apis: string[] = ['api1', 'api2', 'json'];

  query: string;

  result: any;

  replies: any[] = [];
  private selectedApi: string;

  constructor(private http: HttpClient) {
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.scrollToLastReply();
    }, 100);
  }

  ngOnInit(): void {
    this.populateChatHistory();
  }

  sendQuery(query: string) {
    this.replies = [...this.replies, {
      content: query,
      author: 'user'
    }];

    let params = new HttpParams().set('sentence', query);

    console.log('send query???');
    this.http.get('http://localhost:8000/query/' + this.selectedApi, {params: params}).subscribe(result => {
      console.log('result', result);
      this.result = result;
    });

    // this.result = {
    //   userId: 1,
    //   id: 1,
    //   title: 'delectus aut autem',
    //   completed1: false,
    //   completed2: false,
    //   completed3: false,
    //   completed4: false,
    //   completed5: false,
    //   completed6: false,
    //   completed7: false,
    //   completed8: false,
    //   completed9: false,
    //   completed11: false,
    //   completed22: false,
    //   completed33: false,
    //   completed44: false,
    //   completed55: false,
    //   completed66: false,
    //   completed77: false,
    //   completed88: false,
    //   completed99: false,
    //   completed00: false,
    //   completed12: false,
    //   completed13: false
    // };

    setTimeout(() => {
      this.scrollToLastReply();
    }, 1);

  }

  apiSelected(api: string) {
    console.log('selected api', api);
    this.selectedApi = api;
  }

  private populateChatHistory() {
    this.replies.push({
        content: 'Give me all the books',
        author: 'user'
      },
      {
        content: 'Here are all the books',
        author: 'AI'
      },
      {
        content: 'Did I get it right?',
        author: 'AI'
      },
      {
        content: 'No you did not!!!!',
        author: 'user'
      },
      {
        content: 'No you did not!!!!',
        author: 'user'
      },
      {
        content: 'No you did not!!!!',
        author: 'user'
      },
      {
        content: 'No you did not!!!!',
        author: 'user'
      },

      {
        content: 'Hellow',
        author: 'user'
      });
  }

  getReplyUserImage(reply: any) {
    if (reply.author === 'AI') {
      return '../../assets/desktop_mac-24px.svg';
    }

    if (reply.author === 'user') {
      return '../../assets/account_circle-24px.svg';
    }
  }

  private scrollToLastReply() {
    this.repliesDiv.nativeElement.children[this.repliesDiv.nativeElement.children.length - 1].scrollIntoView();
  }

}
