import styles from './style.less';
import router from 'umi/router';
import React from 'react';
import Link from 'umi/link';

function tz(e) {
    router.push(e.target.value);
}

function BasicLayout(props) {
    if(
        RegExp(/^\/$/).exec(props.location.pathname)||
        RegExp(/^\/predict/).exec(props.location.pathname)
    ){
        return(
            <div className={styles.normal}>
                {props.children}
            </div>
        )
    }
    return (
        <div className={styles.normal}>
            <div className={styles.top}>
                <select className={styles.sel} onChange={(e) => tz(e)}>
                    <option value="/a">cp</option>
                    <option value="/b">trestbps</option>
                    <option value="/e">chol</option>
                    <option value="/f">fbs</option>
                    <option value="/g">restecg</option>
                    <option value="/h">thalach</option>
                    <option value="/i">exang</option>
                    <option value="/j">oldpeak</option>
                    <option value="/k">slope</option>
                    <option value="/l">ca</option>
                    <option value="/m">thal</option>
                    <option value="/n">target</option>
                </select>
                <div className={styles.ret}><Link to="/">retrun home</Link></div>
            </div>

            {props.children}
        </div>
    );
}

export default BasicLayout;
