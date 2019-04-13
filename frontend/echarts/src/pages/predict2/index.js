import $ from "jquery";
import React from "react";
import styles from './style.less'
import p1 from '@/assets/FS.png'
import p2 from '@/assets/KNN.png'
import p3 from '@/assets/a2.png'
import Link from 'umi/link';

export default class Jitter extends React.Component {
    state={
        a:1,
        data:null
    }

    componentDidMount(){
        console.log(this.props.match.params,1111)
    }
    handleClick1 = ()=>{
        let ca = this.refs.ca.value;
        let oldpeak = this.refs.oldpeak.value;
        let thalach = this.refs.thalach.value;
        let cp = this.refs.cp.value;
        let exang = this.refs.exang.value;
        let data;
        $.ajax({
            url: "http://127.0.0.1:8888/predict?type=1",
            async : false,
            type:'POST',
            data: JSON.stringify({ca,oldpeak,thalach,cp,exang}),
            contentType:'application/json',
            dataType: "json",
            success: (iData) => {
                this.setState({
                    a:3,
                    data:1
                })
            }
        });

    }
    handleClick2 = ()=>{
        let ca = this.refs.ca.value;
        let oldpeak = this.refs.oldpeak.value;
        let thalach = this.refs.thalach.value;
        let cp = this.refs.cp.value;
        let exang = this.refs.exang.value;
        let data;
        $.ajax({
            url: "http://127.0.0.1:8888/predict?type=2",
            async : false,
            type:'POST',
            data: JSON.stringify({ca,oldpeak,thalach,cp,exang}),
            contentType:'application/json',
            dataType: "json",
            success: (iData) => {
                this.setState({
                    a:3,
                    data:iData.message
                })
            }
        });

    }
    render() {

        return (
            <div className={styles.wrap}>
                <div className={styles.ret}><Link to="/">return</Link></div>
                <div className={styles.con}>
                  <input type="text" ref={'ca'} placeholder="ca"/>
                  <input type="text" ref={'oldpeak'} placeholder="oldpeak"/>
                  <input type="text" ref={'thalach'} placeholder="thalach"/>
                  <input type="text" ref={'cp'} placeholder="cp"/>
                  <input type="text" ref={'exang'} placeholder="exang"/>
                  <div className={styles.btn}>
                    <button onClick={this.handleClick2}>Muti Prediction Submit</button>
                  </div>
                  {this.state.data!==null?(<div className={styles.res}>{this.state.data}</div>):''}
                  <div className={styles.item2}>
                        {
                            this.state.a===1?((<img src={p1} alt=""/>)):this.state.a===2?(<img src={p3} alt=""/>):(
                                <img src={p2} alt=""/>)
                        }
                    </div>
                </div>
            </div>
        );
    }
}
