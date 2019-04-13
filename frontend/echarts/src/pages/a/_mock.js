import mockjs from 'mockjs';

export default {
    // 使用 mockjs 等三方库
    'GET /api/tags': mockjs.mock({
        'list|100': [{ 'cp|1-1010':1, 'age|1-100': 50, 'sex|1': ['男','女'] }],
    }),
};