function jsstart(m_json, m_time) {
   t = fT(m_json, m_time)
   return t
}

class Pt {
    static create(...e) {
        return new this(...e)
    }
    mixIn(e) {
        return Object.assign(this, e)
    }
    clone() {
        const e = new this.constructor;
        return Object.assign(e, this),
        e
    }
}
class Ht extends Pt {
    constructor(e=[], n=e.length * 4) {
        super();
        let o = e;
        if (o instanceof ArrayBuffer && (o = new Uint8Array(o)),
        (o instanceof Int8Array || o instanceof Uint8ClampedArray || o instanceof Int16Array || o instanceof Uint16Array || o instanceof Int32Array || o instanceof Uint32Array || o instanceof Float32Array || o instanceof Float64Array) && (o = new Uint8Array(o.buffer,o.byteOffset,o.byteLength)),
        o instanceof Uint8Array) {
            const r = o.byteLength
              , i = [];
            for (let a = 0; a < r; a += 1)
                i[a >>> 2] |= o[a] << 24 - a % 4 * 8;
            this.words = i,
            this.sigBytes = r
        } else
            this.words = e,
            this.sigBytes = n
    }
    static random(e) {
        const n = []
          , o = r=>{
            let i = r
              , a = 987654321;
            const c = 4294967295;
            return ()=>{
                a = 36969 * (a & 65535) + (a >> 16) & c,
                i = 18e3 * (i & 65535) + (i >> 16) & c;
                let d = (a << 16) + i & c;
                return d /= 4294967296,
                d += .5,
                d * (Math.random() > .5 ? 1 : -1)
            }
        }
        ;
        for (let r = 0, i; r < e; r += 4) {
            const a = o((i || Math.random()) * 4294967296);
            i = a() * 987654071,
            n.push(a() * 4294967296 | 0)
        }
        return new Ht(n,e)
    }
    toString(e=tT) {
        return e.stringify(this)
    }
    concat(e) {
        const n = this.words
          , o = e.words
          , r = this.sigBytes
          , i = e.sigBytes;
        if (this.clamp(),
        r % 4)
            for (let a = 0; a < i; a += 1) {
                const c = o[a >>> 2] >>> 24 - a % 4 * 8 & 255;
                n[r + a >>> 2] |= c << 24 - (r + a) % 4 * 8
            }
        else
            for (let a = 0; a < i; a += 4)
                n[r + a >>> 2] = o[a >>> 2];
        return this.sigBytes += i,
        this
    }
    clamp() {
        const {words: e, sigBytes: n} = this;
        e[n >>> 2] &= 4294967295 << 32 - n % 4 * 8,
        e.length = Math.ceil(n / 4)
    }
    clone() {
        const e = super.clone.call(this);
        return e.words = this.words.slice(0),
        e
    }
}
const tT = {
    stringify(t) {
        const {words: e, sigBytes: n} = t
          , o = [];
        for (let r = 0; r < n; r += 1) {
            const i = e[r >>> 2] >>> 24 - r % 4 * 8 & 255;
            o.push((i >>> 4).toString(16)),
            o.push((i & 15).toString(16))
        }
        return o.join("")
    },
    parse(t) {
        const e = t.length
          , n = [];
        for (let o = 0; o < e; o += 2)
            n[o >>> 3] |= parseInt(t.substr(o, 2), 16) << 24 - o % 8 * 4;
        return new Ht(n,e / 2)
    }
}
  , hm = {
    stringify(t) {
        const {words: e, sigBytes: n} = t
          , o = [];
        for (let r = 0; r < n; r += 1) {
            const i = e[r >>> 2] >>> 24 - r % 4 * 8 & 255;
            o.push(String.fromCharCode(i))
        }
        return o.join("")
    },
    parse(t) {
        const e = t.length
          , n = [];
        for (let o = 0; o < e; o += 1)
            n[o >>> 2] |= (t.charCodeAt(o) & 255) << 24 - o % 4 * 8;
        return new Ht(n,e)
    }
}
  , Bw = {
    stringify(t) {
        try {
            return decodeURIComponent(escape(hm.stringify(t)))
        } catch {
            throw new Error("Malformed UTF-8 data")
        }
    },
    parse(t) {
        return hm.parse(unescape(encodeURIComponent(t)))
    }
};
class Rw extends Pt {
    constructor() {
        super(),
        this._minBufferSize = 0
    }
    reset() {
        this._data = new Ht,
        this._nDataBytes = 0
    }
    _append(e) {
        let n = e;
        typeof n == "string" && (n = Bw.parse(n)),
        this._data.concat(n),
        this._nDataBytes += n.sigBytes
    }
    _process(e) {
        let n;
        const {_data: o, blockSize: r} = this
          , i = o.words
          , a = o.sigBytes
          , c = r * 4;
        let d = a / c;
        e ? d = Math.ceil(d) : d = Math.max((d | 0) - this._minBufferSize, 0);
        const u = d * r
          , h = Math.min(u * 4, a);
        if (u) {
            for (let b = 0; b < u; b += r)
                this._doProcessBlock(i, b);
            n = i.splice(0, u),
            o.sigBytes -= h
        }
        return new Ht(n,h)
    }
    clone() {
        const e = super.clone.call(this);
        return e._data = this._data.clone(),
        e
    }
}
class nT extends Rw {
    constructor(e) {
        super(),
        this.blockSize = 512 / 32,
        this.cfg = Object.assign(new Pt, e),
        this.reset()
    }
    static _createHelper(e) {
        return (n,o)=>new e(o).finalize(n)
    }
    static _createHmacHelper(e) {
        return (n,o)=>new oT(e,o).finalize(n)
    }
    reset() {
        super.reset.call(this),
        this._doReset()
    }
    update(e) {
        return this._append(e),
        this._process(),
        this
    }
    finalize(e) {
        return e && this._append(e),
        this._doFinalize()
    }
}
class oT extends Pt {
    constructor(e, n) {
        super();
        const o = new e;
        this._hasher = o;
        let r = n;
        typeof r == "string" && (r = Bw.parse(r));
        const i = o.blockSize
          , a = i * 4;
        r.sigBytes > a && (r = o.finalize(n)),
        r.clamp();
        const c = r.clone();
        this._oKey = c;
        const d = r.clone();
        this._iKey = d;
        const u = c.words
          , h = d.words;
        for (let b = 0; b < i; b += 1)
            u[b] ^= 1549556828,
            h[b] ^= 909522486;
        c.sigBytes = a,
        d.sigBytes = a,
        this.reset()
    }
    reset() {
        const e = this._hasher;
        e.reset(),
        e.update(this._iKey)
    }
    update(e) {
        return this._hasher.update(e),
        this
    }
    finalize(e) {
        const n = this._hasher
          , o = n.finalize(e);
        return n.reset(),
        n.finalize(this._oKey.clone().concat(o))
    }
}
const rT = (t,e,n)=>{
    const o = [];
    let r = 0;
    for (let i = 0; i < e; i += 1)
        if (i % 4) {
            const a = n[t.charCodeAt(i - 1)] << i % 4 * 2
              , c = n[t.charCodeAt(i)] >>> 6 - i % 4 * 2
              , d = a | c;
            o[r >>> 2] |= d << 24 - r % 4 * 8,
            r += 1
        }
    return Ht.create(o, r)
}
  , mm = {
    stringify(t) {
        const {words: e, sigBytes: n} = t
          , o = this._map;
        t.clamp();
        const r = [];
        for (let a = 0; a < n; a += 3) {
            const c = e[a >>> 2] >>> 24 - a % 4 * 8 & 255
              , d = e[a + 1 >>> 2] >>> 24 - (a + 1) % 4 * 8 & 255
              , u = e[a + 2 >>> 2] >>> 24 - (a + 2) % 4 * 8 & 255
              , h = c << 16 | d << 8 | u;
            for (let b = 0; b < 4 && a + b * .75 < n; b += 1)
                r.push(o.charAt(h >>> 6 * (3 - b) & 63))
        }
        const i = o.charAt(64);
        if (i)
            for (; r.length % 4; )
                r.push(i);
        return r.join("")
    },
    parse(t) {
        let e = t.length;
        const n = this._map;
        let o = this._reverseMap;
        if (!o) {
            this._reverseMap = [],
            o = this._reverseMap;
            for (let i = 0; i < n.length; i += 1)
                o[n.charCodeAt(i)] = i
        }
        const r = n.charAt(64);
        if (r) {
            const i = t.indexOf(r);
            i !== -1 && (e = i)
        }
        return rT(t, e, o)
    },
    _map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
}
  , pe = [];
for (let t = 0; t < 64; t += 1)
    pe[t] = Math.abs(Math.sin(t + 1)) * 4294967296 | 0;
const yt = (t,e,n,o,r,i,a)=>{
    const c = t + (e & n | ~e & o) + r + a;
    return (c << i | c >>> 32 - i) + e
}
  , _t = (t,e,n,o,r,i,a)=>{
    const c = t + (e & o | n & ~o) + r + a;
    return (c << i | c >>> 32 - i) + e
}
  , At = (t,e,n,o,r,i,a)=>{
    const c = t + (e ^ n ^ o) + r + a;
    return (c << i | c >>> 32 - i) + e
}
  , xt = (t,e,n,o,r,i,a)=>{
    const c = t + (n ^ (e | ~o)) + r + a;
    return (c << i | c >>> 32 - i) + e
}
;
class iT extends nT {
    _doReset() {
        this._hash = new Ht([1732584193, 4023233417, 2562383102, 271733878])
    }
    _doProcessBlock(e, n) {
        const o = e;
        for (let le = 0; le < 16; le += 1) {
            const he = n + le
              , be = e[he];
            o[he] = (be << 8 | be >>> 24) & 16711935 | (be << 24 | be >>> 8) & 4278255360
        }
        const r = this._hash.words
          , i = o[n + 0]
          , a = o[n + 1]
          , c = o[n + 2]
          , d = o[n + 3]
          , u = o[n + 4]
          , h = o[n + 5]
          , b = o[n + 6]
          , g = o[n + 7]
          , y = o[n + 8]
          , l = o[n + 9]
          , S = o[n + 10]
          , P = o[n + 11]
          , I = o[n + 12]
          , j = o[n + 13]
          , U = o[n + 14]
          , Y = o[n + 15];
        let T = r[0]
          , D = r[1]
          , N = r[2]
          , G = r[3];
        T = yt(T, D, N, G, i, 7, pe[0]),
        G = yt(G, T, D, N, a, 12, pe[1]),
        N = yt(N, G, T, D, c, 17, pe[2]),
        D = yt(D, N, G, T, d, 22, pe[3]),
        T = yt(T, D, N, G, u, 7, pe[4]),
        G = yt(G, T, D, N, h, 12, pe[5]),
        N = yt(N, G, T, D, b, 17, pe[6]),
        D = yt(D, N, G, T, g, 22, pe[7]),
        T = yt(T, D, N, G, y, 7, pe[8]),
        G = yt(G, T, D, N, l, 12, pe[9]),
        N = yt(N, G, T, D, S, 17, pe[10]),
        D = yt(D, N, G, T, P, 22, pe[11]),
        T = yt(T, D, N, G, I, 7, pe[12]),
        G = yt(G, T, D, N, j, 12, pe[13]),
        N = yt(N, G, T, D, U, 17, pe[14]),
        D = yt(D, N, G, T, Y, 22, pe[15]),
        T = _t(T, D, N, G, a, 5, pe[16]),
        G = _t(G, T, D, N, b, 9, pe[17]),
        N = _t(N, G, T, D, P, 14, pe[18]),
        D = _t(D, N, G, T, i, 20, pe[19]),
        T = _t(T, D, N, G, h, 5, pe[20]),
        G = _t(G, T, D, N, S, 9, pe[21]),
        N = _t(N, G, T, D, Y, 14, pe[22]),
        D = _t(D, N, G, T, u, 20, pe[23]),
        T = _t(T, D, N, G, l, 5, pe[24]),
        G = _t(G, T, D, N, U, 9, pe[25]),
        N = _t(N, G, T, D, d, 14, pe[26]),
        D = _t(D, N, G, T, y, 20, pe[27]),
        T = _t(T, D, N, G, j, 5, pe[28]),
        G = _t(G, T, D, N, c, 9, pe[29]),
        N = _t(N, G, T, D, g, 14, pe[30]),
        D = _t(D, N, G, T, I, 20, pe[31]),
        T = At(T, D, N, G, h, 4, pe[32]),
        G = At(G, T, D, N, y, 11, pe[33]),
        N = At(N, G, T, D, P, 16, pe[34]),
        D = At(D, N, G, T, U, 23, pe[35]),
        T = At(T, D, N, G, a, 4, pe[36]),
        G = At(G, T, D, N, u, 11, pe[37]),
        N = At(N, G, T, D, g, 16, pe[38]),
        D = At(D, N, G, T, S, 23, pe[39]),
        T = At(T, D, N, G, j, 4, pe[40]),
        G = At(G, T, D, N, i, 11, pe[41]),
        N = At(N, G, T, D, d, 16, pe[42]),
        D = At(D, N, G, T, b, 23, pe[43]),
        T = At(T, D, N, G, l, 4, pe[44]),
        G = At(G, T, D, N, I, 11, pe[45]),
        N = At(N, G, T, D, Y, 16, pe[46]),
        D = At(D, N, G, T, c, 23, pe[47]),
        T = xt(T, D, N, G, i, 6, pe[48]),
        G = xt(G, T, D, N, g, 10, pe[49]),
        N = xt(N, G, T, D, U, 15, pe[50]),
        D = xt(D, N, G, T, h, 21, pe[51]),
        T = xt(T, D, N, G, I, 6, pe[52]),
        G = xt(G, T, D, N, d, 10, pe[53]),
        N = xt(N, G, T, D, S, 15, pe[54]),
        D = xt(D, N, G, T, a, 21, pe[55]),
        T = xt(T, D, N, G, y, 6, pe[56]),
        G = xt(G, T, D, N, Y, 10, pe[57]),
        N = xt(N, G, T, D, b, 15, pe[58]),
        D = xt(D, N, G, T, j, 21, pe[59]),
        T = xt(T, D, N, G, u, 6, pe[60]),
        G = xt(G, T, D, N, P, 10, pe[61]),
        N = xt(N, G, T, D, c, 15, pe[62]),
        D = xt(D, N, G, T, l, 21, pe[63]),
        r[0] = r[0] + T | 0,
        r[1] = r[1] + D | 0,
        r[2] = r[2] + N | 0,
        r[3] = r[3] + G | 0
    }
    _doFinalize() {
        const e = this._data
          , n = e.words
          , o = this._nDataBytes * 8
          , r = e.sigBytes * 8;
        n[r >>> 5] |= 128 << 24 - r % 32;
        const i = Math.floor(o / 4294967296)
          , a = o;
        n[(r + 64 >>> 9 << 4) + 15] = (i << 8 | i >>> 24) & 16711935 | (i << 24 | i >>> 8) & 4278255360,
        n[(r + 64 >>> 9 << 4) + 14] = (a << 8 | a >>> 24) & 16711935 | (a << 24 | a >>> 8) & 4278255360,
        e.sigBytes = (n.length + 1) * 4,
        this._process();
        const c = this._hash
          , d = c.words;
        for (let u = 0; u < 4; u += 1) {
            const h = d[u];
            d[u] = (h << 8 | h >>> 24) & 16711935 | (h << 24 | h >>> 8) & 4278255360
        }
        return c
    }
    clone() {
        const e = super.clone.call(this);
        return e._hash = this._hash.clone(),
        e
    }
}
class aT extends Pt {
    constructor(e) {
        super(),
        this.cfg = Object.assign(new Pt, {
            keySize: 128 / 32,
            hasher: iT,
            iterations: 1
        }, e)
    }
    compute(e, n) {
        let o;
        const {cfg: r} = this
          , i = r.hasher.create()
          , a = Ht.create()
          , c = a.words
          , {keySize: d, iterations: u} = r;
        for (; c.length < d; ) {
            o && i.update(o),
            o = i.update(e).finalize(n),
            i.reset();
            for (let h = 1; h < u; h += 1)
                o = i.finalize(o),
                i.reset();
            a.concat(o)
        }
        return a.sigBytes = d * 4,
        a
    }
}
class Zi extends Rw {
    constructor(e, n, o) {
        super(),
        this.cfg = Object.assign(new Pt, o),
        this._xformMode = e,
        this._key = n,
        this.reset()
    }
    static createEncryptor(e, n) {
        return this.create(this._ENC_XFORM_MODE, e, n)
    }
    static createDecryptor(e, n) {
        return this.create(this._DEC_XFORM_MODE, e, n)
    }
    static _createHelper(e) {
        const n = o=>typeof o == "string" ? Nw : Lr;
        return {
            encrypt(o, r, i) {
                return n(r).encrypt(e, o, r, i)
            },
            decrypt(o, r, i) {
                return n(r).decrypt(e, o, r, i)
            }
        }
    }
    reset() {
        super.reset.call(this),
        this._doReset()
    }
    process(e) {
        return this._append(e),
        this._process()
    }
    finalize(e) {
        return e && this._append(e),
        this._doFinalize()
    }
}
Zi._ENC_XFORM_MODE = 1;
Zi._DEC_XFORM_MODE = 2;
Zi.keySize = 128 / 32;
Zi.ivSize = 128 / 32;
class sT extends Pt {
    constructor(e, n) {
        super(),
        this._cipher = e,
        this._iv = n
    }
    static createEncryptor(e, n) {
        return this.Encryptor.create(e, n)
    }
    static createDecryptor(e, n) {
        return this.Decryptor.create(e, n)
    }
}
function Lw(t, e, n) {
    const o = t;
    let r;
    const i = this._iv;
    i ? (r = i,
    this._iv = void 0) : r = this._prevBlock;
    for (let a = 0; a < n; a += 1)
        o[e + a] ^= r[a]
}
class Ri extends sT {
}
Ri.Encryptor = class extends Ri {
    processBlock(t, e) {
        const n = this._cipher
          , {blockSize: o} = n;
        Lw.call(this, t, e, o),
        n.encryptBlock(t, e),
        this._prevBlock = t.slice(e, e + o)
    }
}
;
Ri.Decryptor = class extends Ri {
    processBlock(t, e) {
        const n = this._cipher
          , {blockSize: o} = n
          , r = t.slice(e, e + o);
        n.decryptBlock(t, e),
        Lw.call(this, t, e, o),
        this._prevBlock = r
    }
}
;
const cT = {
    pad(t, e) {
        const n = e * 4
          , o = n - t.sigBytes % n
          , r = o << 24 | o << 16 | o << 8 | o
          , i = [];
        for (let c = 0; c < o; c += 4)
            i.push(r);
        const a = Ht.create(i, o);
        t.concat(a)
    },
    unpad(t) {
        const e = t
          , n = e.words[e.sigBytes - 1 >>> 2] & 255;
        e.sigBytes -= n
    }
};
class Mw extends Zi {
    constructor(e, n, o) {
        super(e, n, Object.assign({
            mode: Ri,
            padding: cT
        }, o)),
        this.blockSize = 128 / 32
    }
    reset() {
        let e;
        super.reset.call(this);
        const {cfg: n} = this
          , {iv: o, mode: r} = n;
        this._xformMode === this.constructor._ENC_XFORM_MODE ? e = r.createEncryptor : (e = r.createDecryptor,
        this._minBufferSize = 1),
        this._mode = e.call(r, this, o && o.words),
        this._mode.__creator = e
    }
    _doProcessBlock(e, n) {
        this._mode.processBlock(e, n)
    }
    _doFinalize() {
        let e;
        const {padding: n} = this.cfg;
        return this._xformMode === this.constructor._ENC_XFORM_MODE ? (n.pad(this._data, this.blockSize),
        e = this._process(!0)) : (e = this._process(!0),
        n.unpad(e)),
        e
    }
}
class du extends Pt {
    constructor(e) {
        super(),
        this.mixIn(e)
    }
    toString(e) {
        return (e || this.formatter).stringify(this)
    }
}
const lT = {
    stringify(t) {
        let e;
        const {ciphertext: n, salt: o} = t;
        return o ? e = Ht.create([1398893684, 1701076831]).concat(o).concat(n) : e = n,
        e.toString(mm)
    },
    parse(t) {
        let e;
        const n = mm.parse(t)
          , o = n.words;
        return o[0] === 1398893684 && o[1] === 1701076831 && (e = Ht.create(o.slice(2, 4)),
        o.splice(0, 4),
        n.sigBytes -= 16),
        du.create({
            ciphertext: n,
            salt: e
        })
    }
};
class Lr extends Pt {
    static encrypt(e, n, o, r) {
        const i = Object.assign(new Pt, this.cfg, r)
          , a = e.createEncryptor(o, i)
          , c = a.finalize(n)
          , d = a.cfg;
        return du.create({
            ciphertext: c,
            key: o,
            iv: d.iv,
            algorithm: e,
            mode: d.mode,
            padding: d.padding,
            blockSize: a.blockSize,
            formatter: i.format
        })
    }
    static decrypt(e, n, o, r) {
        let i = n;
        const a = Object.assign(new Pt, this.cfg, r);
        return i = this._parse(i, a.format),
        e.createDecryptor(o, a).finalize(i.ciphertext)
    }
    static _parse(e, n) {
        return typeof e == "string" ? n.parse(e, this) : e
    }
}
Lr.cfg = Object.assign(new Pt, {
    format: lT
});
const dT = {
    execute(t, e, n, o) {
        let r = o;
        r || (r = Ht.random(64 / 8));
        const i = aT.create({
            keySize: e + n
        }).compute(t, r)
          , a = Ht.create(i.words.slice(e), n * 4);
        return i.sigBytes = e * 4,
        du.create({
            key: i,
            iv: a,
            salt: r
        })
    }
};
class Nw extends Lr {
    static encrypt(e, n, o, r) {
        const i = Object.assign(new Pt, this.cfg, r)
          , a = i.kdf.execute(o, e.keySize, e.ivSize);
        i.iv = a.iv;
        const c = Lr.encrypt.call(this, e, n, a.key, i);
        return c.mixIn(a),
        c
    }
    static decrypt(e, n, o, r) {
        let i = n;
        const a = Object.assign(new Pt, this.cfg, r);
        i = this._parse(i, a.format);
        const c = a.kdf.execute(o, e.keySize, e.ivSize, i.salt);
        return a.iv = c.iv,
        Lr.decrypt.call(this, e, i, c.key, a)
    }
}
Nw.cfg = Object.assign(Lr.cfg, {
    kdf: dT
});
const Lt = []
  , jw = []
  , zw = []
  , Fw = []
  , Uw = []
  , Gw = []
  , Hd = []
  , Wd = []
  , Vd = []
  , qd = []
  , An = [];
for (let t = 0; t < 256; t += 1)
    t < 128 ? An[t] = t << 1 : An[t] = t << 1 ^ 283;
let _n = 0
  , Wn = 0;
for (let t = 0; t < 256; t += 1) {
    let e = Wn ^ Wn << 1 ^ Wn << 2 ^ Wn << 3 ^ Wn << 4;
    e = e >>> 8 ^ e & 255 ^ 99,
    Lt[_n] = e,
    jw[e] = _n;
    const n = An[_n]
      , o = An[n]
      , r = An[o];
    let i = An[e] * 257 ^ e * 16843008;
    zw[_n] = i << 24 | i >>> 8,
    Fw[_n] = i << 16 | i >>> 16,
    Uw[_n] = i << 8 | i >>> 24,
    Gw[_n] = i,
    i = r * 16843009 ^ o * 65537 ^ n * 257 ^ _n * 16843008,
    Hd[e] = i << 24 | i >>> 8,
    Wd[e] = i << 16 | i >>> 16,
    Vd[e] = i << 8 | i >>> 24,
    qd[e] = i,
    _n ? (_n = n ^ An[An[An[r ^ n]]],
    Wn ^= An[An[Wn]]) : (Wn = 1,
    _n = Wn)
}
const pT = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54];
class Hw extends Mw {
    _doReset() {
        let e;
        if (this._nRounds && this._keyPriorReset === this._key)
            return;
        this._keyPriorReset = this._key;
        const n = this._keyPriorReset
          , o = n.words
          , r = n.sigBytes / 4;
        this._nRounds = r + 6;
        const a = (this._nRounds + 1) * 4;
        this._keySchedule = [];
        const c = this._keySchedule;
        for (let u = 0; u < a; u += 1)
            u < r ? c[u] = o[u] : (e = c[u - 1],
            u % r ? r > 6 && u % r === 4 && (e = Lt[e >>> 24] << 24 | Lt[e >>> 16 & 255] << 16 | Lt[e >>> 8 & 255] << 8 | Lt[e & 255]) : (e = e << 8 | e >>> 24,
            e = Lt[e >>> 24] << 24 | Lt[e >>> 16 & 255] << 16 | Lt[e >>> 8 & 255] << 8 | Lt[e & 255],
            e ^= pT[u / r | 0] << 24),
            c[u] = c[u - r] ^ e);
        this._invKeySchedule = [];
        const d = this._invKeySchedule;
        for (let u = 0; u < a; u += 1) {
            const h = a - u;
            u % 4 ? e = c[h] : e = c[h - 4],
            u < 4 || h <= 4 ? d[u] = e : d[u] = Hd[Lt[e >>> 24]] ^ Wd[Lt[e >>> 16 & 255]] ^ Vd[Lt[e >>> 8 & 255]] ^ qd[Lt[e & 255]]
        }
    }
    encryptBlock(e, n) {
        this._doCryptBlock(e, n, this._keySchedule, zw, Fw, Uw, Gw, Lt)
    }
    decryptBlock(e, n) {
        const o = e;
        let r = o[n + 1];
        o[n + 1] = o[n + 3],
        o[n + 3] = r,
        this._doCryptBlock(o, n, this._invKeySchedule, Hd, Wd, Vd, qd, jw),
        r = o[n + 1],
        o[n + 1] = o[n + 3],
        o[n + 3] = r
    }
    _doCryptBlock(e, n, o, r, i, a, c, d) {
        const u = e
          , h = this._nRounds;
        let b = u[n] ^ o[0]
          , g = u[n + 1] ^ o[1]
          , y = u[n + 2] ^ o[2]
          , l = u[n + 3] ^ o[3]
          , S = 4;
        for (let Y = 1; Y < h; Y += 1) {
            const T = r[b >>> 24] ^ i[g >>> 16 & 255] ^ a[y >>> 8 & 255] ^ c[l & 255] ^ o[S];
            S += 1;
            const D = r[g >>> 24] ^ i[y >>> 16 & 255] ^ a[l >>> 8 & 255] ^ c[b & 255] ^ o[S];
            S += 1;
            const N = r[y >>> 24] ^ i[l >>> 16 & 255] ^ a[b >>> 8 & 255] ^ c[g & 255] ^ o[S];
            S += 1;
            const G = r[l >>> 24] ^ i[b >>> 16 & 255] ^ a[g >>> 8 & 255] ^ c[y & 255] ^ o[S];
            S += 1,
            b = T,
            g = D,
            y = N,
            l = G
        }
        const P = (d[b >>> 24] << 24 | d[g >>> 16 & 255] << 16 | d[y >>> 8 & 255] << 8 | d[l & 255]) ^ o[S];
        S += 1;
        const I = (d[g >>> 24] << 24 | d[y >>> 16 & 255] << 16 | d[l >>> 8 & 255] << 8 | d[b & 255]) ^ o[S];
        S += 1;
        const j = (d[y >>> 24] << 24 | d[l >>> 16 & 255] << 16 | d[b >>> 8 & 255] << 8 | d[g & 255]) ^ o[S];
        S += 1;
        const U = (d[l >>> 24] << 24 | d[b >>> 16 & 255] << 16 | d[g >>> 8 & 255] << 8 | d[y & 255]) ^ o[S];
        S += 1,
        u[n] = P,
        u[n + 1] = I,
        u[n + 2] = j,
        u[n + 3] = U
    }
}
Hw.keySize = 256 / 32;
const uT = Mw._createHelper(Hw)
  , fT = (t,e)=>{
    const
      o = ["f", 7, 7, 8, "b", "0", "2", 7, "c", "0", 8, "a", "6", "c", String(10086).length + 3]
      , r = ["Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1", "f778b027c08a6c8"]
    return t = "dcoding://" + uT.encrypt(JSON.stringify(t), "f2741610a30040c7a" + r[1] + ":" + e).toString(),
    t
}