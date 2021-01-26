import {AfterViewInit, ChangeDetectorRef, Component, OnInit, ViewChild} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {FormControl, Validators} from '@angular/forms';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewInit {

  @ViewChild('repliesList') repliesList;
  @ViewChild('repliesDiv') repliesDiv;

  apis: string[] = ['json', 'questions'];

  query: string;

  result: any;

  replies: any[] = [];
  private selectedApi: string;

  recognition;
  speechRecognitionList;
  private baseApiUrl: string = 'http://localhost:8000';

  constructor(private http: HttpClient,
              private _cdr: ChangeDetectorRef,
              private _snackBar: MatSnackBar) {
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.scrollToLastReply();
    }, 100);
  }

  ngOnInit(): void {
    this.populateChatHistory();
    this.initSpeechRecognition();
  }

  sendQuery(query: string) {

    if (!this.selectedApi) {
      this._snackBar.open('Please select an API', '', {
        duration: 2000,
      });

      return;
    }

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

  startListening() {
    this.query = 'ciao';
    console.log('starting speech recognition');
    this.recognition.start();
  }


  private initSpeechRecognition() {
    var SpeechRecognition = SpeechRecognition || window['webkitSpeechRecognition'];
    var SpeechGrammarList = SpeechGrammarList || window['webkitSpeechGrammarList'];

    this.recognition = new SpeechRecognition();
    this.speechRecognitionList = new SpeechGrammarList();
    this.recognition.grammars = this.speechRecognitionList;
    this.recognition.continuous = true;
    this.recognition.lang = 'en-US';
    this.recognition.interimResults = true;
    this.recognition.maxAlternatives = 1;

    let that = this;
    this.recognition.onresult = function(event) {
      for (var i = event.resultIndex; i < event.results.length; i++) {
        that.query = event.results[i][0].transcript;
        that._cdr.detectChanges();
      }
    };

    this.recognition.onspeechend = function() {
      that.recognition.stop();
    };

    this.recognition.onnomatch = function(event) {
      console.log('did not recognize', event);
    };

    this.recognition.onerror = function(event) {
      console.log('error', event);
    };
  }

  onChange(event: Event) {
    var file = event.target.files[0];

    if (!file) {
      return;
    }

    const formData = new FormData();

    formData.append("file", file, file.name);

    this.http.post(this.baseApiUrl + '/upload/', formData).subscribe(response =>
    this.apis.push(file.name.split('.')[0]));
  }

}
